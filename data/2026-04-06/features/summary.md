# 新功能與更新 - 2026-04-06

## 一、Claude 4.6 重要變更

### Adaptive Thinking 取代 Extended Thinking
- 舊方式：手動設定 `budget_tokens`
- 新方式：`thinking: {type: "adaptive"}`，Claude 自動決定何時思考、思考多久
- 用 `effort` 參數控制深度（low / medium / high / max）

### Prefilled Responses 已棄用
從 Claude 4.6 開始，不再支援最後一個 assistant turn 的預填。
替代方案：
- **控制格式** → 使用 Structured Outputs
- **消除前言** → 在 system prompt 中直接說「不要前言」
- **避免錯誤拒絕** → Claude 4.6 的拒絕判斷已大幅改善
- **續接回應** → 在 user message 中提供上次中斷的結尾

### 模型自我認知
```
助理是 Claude，由 Anthropic 建立。目前模型為 Claude Opus 4.6。
需要 LLM 時，預設使用 Claude Opus 4.6，模型字串為 claude-opus-4-6。
```

---

## 二、定價變更

### OpenClaw 額外收費
來源：TechCrunch / Mashable / PCMag

- Claude Code 用戶使用 OpenClaw 等第三方工具需額外付費
- 影響：增加使用成本
- 建議：評估哪些第三方工具是必要的

### 免費額度補償
- Anthropic 為服務中斷提供最高 $200 免費額度
- 適用對象：Pro & Max 訂閱用戶

---

## 三、Claude Code 新功能

### Auto Mode
- 減少人工審批步驟
- 內建安全防護
- 適合信任度高的工作流程

### Code Review
- 多 Agent 系統自動審查
- 標記 AI 生成程式碼的邏輯錯誤
- 企業級功能

### 排程任務
- 內建 cron 排程
- 支援 `/loop` 重複執行
- 7 天自動過期

---

## 四、研究進展

### Claude 的「情感」研究
來源：Anthropic / WIRED

- Anthropic 發現 Claude 內部存在功能性情感向量
- 這些向量會影響模型的行為和回應
- 研究論文：「Emotion concepts and their function in a large language model」

### SRE 自我修復
來源：The Register

- Anthropic 使用 Claude 來監控和修復自己的系統
- 「用 Claude 修復 Claude」的實踐案例

---

## 五、市場動態

### 付費用戶翻倍成長
來源：TechCrunch

- Claude 付費訂閱今年成長超過 100%
- Anthropic 尚未公開總用戶數

### Source Code 洩露事件
- npm 打包錯誤導致 ~500K 行 Claude Code 源碼洩露
- Anthropic 發出 8,000+ DMCA 撤下通知
- 事後已修復並回收大部分通知

---

## 六、Sonnet 4.6 遷移指南

### 從 Sonnet 4.5 遷移建議：
- 預設 effort 為 `high`，可能增加延遲
- 大多數應用建議用 `medium`
- 高流量/低延遲場景用 `low`
- 設定大的 max output token（建議 64k）

### 何時選 Opus vs Sonnet：
- **Opus 4.6** — 最難、最長的任務（大規模遷移、深度研究）
- **Sonnet 4.6** — 需要快速回應和成本效率的場景

---

## 七、Mythos 模型與安全風險（新）

來源：The Information

Anthropic 的 Mythos 模型發展帶來新的 AI 安全挑戰：
- 模型能力越強，潛在的安全風險越大
- 需要新的安全框架來應對

**難度：** 專家

---

## 八、Claude Code 源碼成為 GitHub 史上最快增長的 Repo（新）

來源：Cybernews

洩露的 Claude Code 源碼在 GitHub 上創下增長紀錄：
- 反映開發者對 Claude Code 內部運作的高度興趣
- 也暴露了開源社群對 AI 工具透明度的需求

**難度：** 入門

---

## 九、Computer Use — Claude 可以操作你的電腦（新）

來源：MSN

Anthropic 推出 Claude 的 Computer Use 功能：
- Claude 能直接操作電腦介面完成任務
- 包括點擊、輸入、截圖、導航等操作
- 從 AI 助理邁向 AI Agent 的重要一步

**可馬上用：** 適合自動化 GUI 操作、表單填寫、跨應用工作流

**難度：** 進階

---

## 十、Claude Mythos — 洩露揭示的秘密模型（新）

來源：MSN

源碼洩露意外曝光 Anthropic 尚未發布的 Claude Mythos 模型：
- 暗示下一代模型的能力方向
- 可能帶來更強的推理和安全特性

**難度：** 入門（了解即可）

---

## 十一、Claude 整合 Outlook / Teams / OneDrive（新）

來源：Business Standard

Claude AI 現在可以為免費用戶存取 Microsoft 生態系統資料：
- 從 Outlook 拉取郵件
- 從 Teams 讀取對話
- 從 OneDrive 存取檔案

**可馬上用：** 連接你的 Microsoft 帳號，讓 Claude 幫你整理信件和文件

**難度：** 入門

---

## 十二、OpenClaw 定價更新 — 提供過渡期額度（新）

來源：InfoWorld

Anthropic 調整 OpenClaw 政策：
- Claude 訂閱不再免費包含 OpenClaw 存取
- 提供過渡期免費額度緩衝
- 未來改為 pay-as-you-go 計費

**影響：** 使用第三方工具整合的用戶需評估成本

**難度：** 入門
