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
