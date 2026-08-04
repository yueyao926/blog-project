const {
  Notice,
  Plugin,
  PluginSettingTab,
  Setting,
  requestUrl,
} = require("obsidian");

const DEFAULT_SETTINGS = {
  apiUrl: "http://localhost/api",
  apiToken: "",
};

module.exports = class DirectBlogPublisher extends Plugin {
  async onload() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    this.addSettingTab(new PublisherSettingTab(this.app, this));
    this.addCommand({
      id: "publish-current-note",
      name: "发布/更新当前文章到博客",
      callback: () => this.publishCurrentNote(),
    });
  }

  async api(path, body) {
    const base = this.settings.apiUrl.replace(/\/$/, "");
    try {
      const response = await requestUrl({
        url: `${base}${path}`,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Obsidian-Token": this.settings.apiToken,
        },
        body: JSON.stringify(body),
        throw: false,
      });
      if (response.status < 200 || response.status >= 300) {
        const detail = response.json?.detail || response.text || `HTTP ${response.status}`;
        throw new Error(detail);
      }
      return response.json;
    } catch (error) {
      throw new Error(`博客接口请求失败：${error.message}`);
    }
  }

  async uploadImage(file) {
    const bytes = await this.app.vault.readBinary(file);
    let binary = "";
    const view = new Uint8Array(bytes);
    for (let i = 0; i < view.length; i += 0x8000) {
      binary += String.fromCharCode(...view.subarray(i, i + 0x8000));
    }
    const result = await this.api("/integrations/obsidian/assets", {
      filename: file.name,
      content_base64: btoa(binary),
    });
    return result.url;
  }

  async replaceLocalImages(markdown, sourceFile) {
    const replacements = [];
    const wiki = /!\[\[([^\]|]+)(?:\|[^\]]*)?\]\]/g;
    const standard = /!\[([^\]]*)\]\((?!https?:\/\/|data:)([^)]+)\)/g;

    for (const match of markdown.matchAll(wiki)) {
      replacements.push({ full: match[0], alt: "", link: match[1] });
    }
    for (const match of markdown.matchAll(standard)) {
      replacements.push({ full: match[0], alt: match[1], link: decodeURIComponent(match[2]) });
    }

    const uploaded = new Map();
    for (const item of replacements) {
      const cleanLink = item.link.split("#")[0];
      const file = this.app.metadataCache.getFirstLinkpathDest(cleanLink, sourceFile.path);
      if (!file) throw new Error(`找不到本地图片：${item.link}`);
      if (!uploaded.has(file.path)) uploaded.set(file.path, await this.uploadImage(file));
      markdown = markdown.replace(item.full, `![${item.alt}](${uploaded.get(file.path)})`);
    }
    return markdown;
  }

  async publishCurrentNote() {
    const file = this.app.workspace.getActiveFile();
    if (!file || file.extension !== "md") return new Notice("请先打开一篇 Markdown 笔记");
    if (!this.settings.apiToken) return new Notice("请先在插件设置中填写 API Token");

    const notice = new Notice("正在上传图片并发布文章…", 0);
    try {
      const raw = await this.app.vault.read(file);
      const cache = this.app.metadataCache.getFileCache(file);
      const frontmatter = cache?.frontmatter || {};
      let content = raw.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, "");
      content = await this.replaceLocalImages(content, file);

      const result = await this.api("/integrations/obsidian/articles", {
        article_id: frontmatter.blog_article_id ? Number(frontmatter.blog_article_id) : null,
        title: String(frontmatter.title || file.basename),
        summary: String(frontmatter.summary || ""),
        cover_image: frontmatter.cover_image ? String(frontmatter.cover_image) : null,
        category_id: frontmatter.category_id == null ? null : Number(frontmatter.category_id),
        content,
      });

      await this.app.fileManager.processFrontMatter(file, (fm) => {
        fm.blog_article_id = result.article_id;
        fm.blog_url = result.article_url;
      });
      notice.hide();
      new Notice(result.created ? "文章已发布，预览链接已写回属性" : "文章已更新，预览链接已写回属性", 6000);
    } catch (error) {
      notice.hide();
      new Notice(error.message, 10000);
      console.error("Direct Blog Publisher", error);
    }
  }
};

class PublisherSettingTab extends PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display() {
    this.containerEl.empty();
    new Setting(this.containerEl)
      .setName("博客 API 地址")
      .setDesc("本地 Docker 默认为 http://localhost/api；线上填写 https://你的域名/api")
      .addText((text) => text.setValue(this.plugin.settings.apiUrl).onChange(async (value) => {
        this.plugin.settings.apiUrl = value.trim();
        await this.plugin.saveData(this.plugin.settings);
      }));
    new Setting(this.containerEl)
      .setName("API Token")
      .setDesc("与博客服务端 OBSIDIAN_API_TOKEN 完全一致")
      .addText((text) => {
        text.inputEl.type = "password";
        return text.setValue(this.plugin.settings.apiToken).onChange(async (value) => {
          this.plugin.settings.apiToken = value.trim();
          await this.plugin.saveData(this.plugin.settings);
        });
      });
  }
}
