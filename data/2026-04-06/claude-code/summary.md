# Claude Code 使用技巧 - 2026-04-06

## 一、核心工作流程

### 排程任務（Scheduled Tasks）
來源：XDA「Claude's scheduled tasks finally fixed what ChatGPT got wrong」

Claude Code 支援定時任務功能：
- 使用 `/loop` 建立重複執行的排程
- 使用 `CronCreate` 設定 cron 表達式
- 適合：定期檢查、自動化收集、監控任務

**可直接使用的範例：**
```
/loop 10m 檢查部署狀態並回報
/loop 1h 收集最新技術新聞
```

**難度：** 進階

---

### Auto Mode（自動模式）
來源：TechCrunch「Anthropic hands Claude Code more control, but keeps it on a leash」

新功能讓 Claude Code 能以更少的人工審批執行任務：
- 減少逐步確認的次數
- 內建安全防護機制
- 適合信任度高的重複性工作

**難度：** 進階

---

### Code Review 功能
來源：TechCrunch「Anthropic launches code review tool」

Claude Code 內建多 Agent 程式碼審查系統：
- 自動分析 AI 生成的程式碼
- 標記邏輯錯誤
- 適合企業級開發流程

**難度：** 進階

---

## 二、CLAUDE.md 最佳實踐

根據官方文件，CLAUDE.md 是專案的「記憶檔案」：

### 應該放什麼：
- 專案建置與測試指令
- 程式碼風格偏好
- 重要的架構決策
- 常用工具與工作流程

### 不應該放什麼：
- 可從程式碼推導的資訊
- Git 歷史（用 git log 查）
- 暫時性的任務狀態

**範例結構：**
```markdown
# 專案名稱

## 建置
npm install && npm run dev

## 測試
npm test

## 風格
- 使用 TypeScript strict mode
- 偏好函數式風格
- 測試使用 vitest

## 架構
- src/api/ — API 路由
- src/components/ — React 元件
```

**難度：** 入門

---

## 三、平行工具呼叫

Claude 4.6 擅長平行執行多個工具：
- 同時讀取多個檔案
- 同時執行多個搜尋
- 同時運行多個 bash 指令

**提升效率的 prompt：**
```
如果要呼叫多個工具且彼此之間沒有依賴關係，請同時並行呼叫所有獨立的工具。
```

**難度：** 進階

---

## 四、長時間任務管理

### 跨 Context Window 工作
Claude 4.6 支援跨多個 context window 的長期任務：

1. **第一個 window** — 建立框架（寫測試、建立腳本）
2. **後續 window** — 基於 todo list 迭代
3. **使用 git 追蹤狀態** — 提供檢查點和復原能力
4. **寫進度筆記** — 用 progress.txt 記錄進度

**重要提示：**
```
你的 context window 接近極限時會自動壓縮，允許你繼續工作。
因此不要因為 token 預算擔憂而提早停止任務。
```

**難度：** 專家

---

## 五、Sub-Agent 協作

Claude 4.6 會自動判斷何時需要委派子任務給 sub-agent：

### 適合使用 Sub-Agent：
- 可平行執行的任務
- 需要隔離 context 的工作
- 獨立的工作流程

### 不適合使用：
- 簡單的單一操作（直接 grep 更快）
- 需要跨步驟共享狀態的任務
- 單檔案編輯

**難度：** 專家

---

## 六、Top 50 Claude Skills & GitHub Repos

來源：Blockchain Council 整理的 2026 年精選資源

涵蓋：
- 常用 slash commands
- MCP server 設定
- 自動化工作流模板
- 社群開發的實用工具

[完整清單需進一步查閱]

**難度：** 入門～專家

---

## 七、System Prompt 解析（新）

來源：dbreunig.com「How Claude Code builds a system prompt」

深度分析 Claude Code 如何建構 system prompt：
- 揭示 Claude Code 的內部 prompt 組裝邏輯
- 理解各層 prompt 的優先級和作用
- 學習如何更好地配合 Claude Code 的 prompt 結構

**可馬上用：** 了解 system prompt 結構後，寫出更精確的 CLAUDE.md

**難度：** 進階

---

## 八、社群熱門 Skills 精選（新）

### Grug Skill — 簡單至上的開發哲學
來源：[github.com/replete/grug-skill](https://github.com/replete/grug-skill)

基於「Grug Brained Developer」哲學的 Claude Code skill：
- 強調簡單、直接、避免過度工程
- 適合想減少 Claude 過度設計傾向的開發者

**難度：** 入門

### Crabby — 像 Rust 編譯器一樣審查程式碼
來源：Hacker News

讓 Claude 以 rustc 錯誤格式輸出診斷回饋：
- 精確的建議和修復方案
- 適合 Rust 開發者或喜歡嚴格審查的團隊

**難度：** 進階

### /Render — 3D 模型技能
來源：[github.com/mfranzon/render](https://github.com/mfranzon/render)

讓 Claude Code 具備 3D 模型渲染和視覺化能力。

**難度：** 進階

### AI Image Creator Skill — 圖像生成教學
來源：ai.georgeliu.com

完整教學：如何為 Claude Code 開發圖像生成技能。

**可馬上用：** 按照教學步驟建立自己的圖像生成 skill

**難度：** 進階

### Unix Conventions Skill — 保持 Unix 風格
來源：[github.com/agiacalone/unix-conventions](https://github.com/agiacalone/unix-conventions)

讓 Claude Code 遵循傳統 Unix 設計原則。

**難度：** 入門

---

## 九、進階整合工具（新）

### LLM Router — 將任務路由到更便宜的模型
來源：[github.com/ypollak2/llm-router](https://github.com/ypollak2/llm-router)

MCP server，自動將 Claude Code 任務分配到成本更低的模型：
- 節省 API 費用
- 簡單任務用小模型，複雜任務用 Opus

**可馬上用：** 安裝後立即降低 Claude Code 使用成本

**難度：** 進階

### VibeAround — 從 Telegram 操作 Claude Code
來源：[github.com/jazzenchen/VibeAround](https://github.com/jazzenchen/VibeAround)

Telegram 整合，支援 session 移交：
- 手機上遠端控制 Claude Code
- 多裝置之間無縫切換

**難度：** 進階

### Tandem — 非程式碼文件的即時協作 IDE
來源：[github.com/bloknayrb/tandem](https://github.com/bloknayrb/tandem)

專為文件協作設計的 IDE，與 Claude Code 整合：
- 適合文件撰寫、規劃、筆記
- 即時協作功能

**難度：** 入門

### Running Gemma 4 locally with Claude Code
來源：ai.georgeliu.com

教學：使用 LM Studio 的 headless CLI 在本地運行 Gemma 4，並與 Claude Code 整合：
- 本地 LLM + Claude Code 的混合工作流
- 降低 API 依賴

**可馬上用：** 安裝 LM Studio → 下載 Gemma 4 → 配合 Claude Code 使用

**難度：** 專家

---

## 十、Claude Code 與競品比較（新）

來源：XDA「I used Claude Code, Antigravity, and Perplexity Computer to build a portfolio」

實測比較 Claude Code vs Antigravity vs Perplexity Computer：
- Claude Code 在專案建構上被評為最佳
- 優勢：更強的程式碼品質和上下文理解

**難度：** 入門
