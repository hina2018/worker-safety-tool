import streamlit as st

# ページ設定
st.set_page_config(
    page_title="ワーカー向け案件安全化ツール",
    page_icon="📋",
    layout="wide"
)

# パスワード認証
def check_password():
    def password_entered():
        if st.session_state["password"] == "worker2024":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # ウェルカム画面
        st.markdown("<h1 style='text-align: center;'>📋 ワーカー向け案件安全化ツール</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #666;'>案件選びから納品まで、非承認・修正リスクを最小化</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        # 中央寄せのコンテナ
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 購入者専用ページ")
            st.markdown("パスワードを入力してツールにアクセスしてください")
            st.text_input(
                "パスワード",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="購入時にお送りしたパスワードを入力"
            )
            st.info("💡 パスワードは購入時のメールに記載されています")
        
        return False
    elif not st.session_state["password_correct"]:
        # エラー時の画面
        st.markdown("<h1 style='text-align: center;'>📋 ワーカー向け案件安全化ツール</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #666;'>案件選びから納品まで、非承認・修正リスクを最小化</h3>", unsafe_allow_html=True)
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 購入者専用ページ")
            st.markdown("パスワードを入力してツールにアクセスしてください")
            st.text_input(
                "パスワード",
                type="password",
                on_change=password_entered,
                key="password",
                placeholder="購入時にお送りしたパスワードを入力"
            )
            st.error("❌ パスワードが違います。もう一度お試しください。")
            st.info("💡 パスワードは購入時のメールに記載されています")
        
        return False
    else:
        return True

if check_password():
    # タイトル
    st.title("📋 ワーカー向け案件安全化ツール")
    st.markdown("### 案件選びから納品まで、非承認・修正リスクを最小化")
    
    # サイドバー
    st.sidebar.title("📂 作業フェーズ")
    st.sidebar.markdown("現在のフェーズを選択:")
    
    phase = st.sidebar.radio(
        "",
        ["① 案件探し（時給・地雷判定）", "② 契約後（指示の確認）", "③ 執筆・納品（検品）"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("💡 使い方の流れ")
    st.sidebar.markdown("""
    **①案件探し（応募前）**  
    募集文を見て「受けるべき？」→判定
    
    ↓
    
    **②契約後（着手前）**  
    詳細指示「不明点ないか？」→確認
    
    ↓
    
    **③執筆・納品（完成後）**  
    納品前「これで大丈夫？」→検品
    """)
    
    # フェーズ①: 案件探し
    if "① 案件探し" in phase:
        st.header("① 案件探しフェーズ: 時給・地雷判定")
        st.markdown("**目的**: 損する案件をスルーし、「勝てる案件」だけに集中")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 入力エリア")
            
            # 募集文入力
            job_description = st.text_area(
                "募集文をコピペ（必須）",
                height=300,
                placeholder="クラウドワークスやランサーズの案件募集文をそのままコピペしてください",
                help="案件ページの募集文全体をコピーして貼り付けてください"
            )
            
            # あなたの情報
            st.markdown("---")
            st.markdown("**あなたの情報**")
            
            col_a, col_b = st.columns(2)
            with col_a:
                work_speed = st.selectbox(
                    "作業スピード",
                    ["遅い", "普通", "速い"],
                    index=1
                )
            with col_b:
                desired_hourly_rate = st.number_input(
                    "希望時給（円）",
                    min_value=500,
                    max_value=5000,
                    value=1000,
                    step=100
                )
            
            genre = st.text_input(
                "得意ジャンル（任意）",
                placeholder="例: 美容、金融、育児 など",
                help="入力すると、得意分野との相性を判断し、より精密な作業時間・時給を計算できます。未入力でも問題ありません。"
            )
        
        with col2:
            st.subheader("🎨 生成されたプロンプト")
            
            if st.button("🔮 プロンプト生成", type="primary", use_container_width=True):
                if not job_description:
                    st.error("募集文を入力してください")
                else:
                    # プロンプト生成
                    prompt = f"""以下の案件募集文を分析して、低単価ワーカー向けに「受注すべきか判断する情報」を提供してください。

【募集文】
{job_description}

【あなたの情報】
- 作業スピード: {work_speed}
- 希望時給: {desired_hourly_rate}円
- ジャンル: {genre if genre else "なし"}

以下の形式で出力してください：

---
## 📊 案件分析結果

### 1. 作業内容の分解
- リサーチ: XX分
- 執筆: XX分  
- 修正: XX分
- その他: XX分

### 2. 推定作業時間
合計: XX時間XX分

### 3. 推定時給
約XX円/時間

### 4. 地雷判定 ⭐️（1〜5）
⭐️⭐️⭐️⭐️⭐️

### 5. 総合評価
【推奨】受注する / スルー推奨

### 6. 注意点コメント
- （修正リスクや曖昧な指示について具体的に指摘）
- （初心者が見落としがちなポイント）
- （クライアントの傾向予測）

### 7. 受注時のアドバイス
- （受注する場合の対策）
---

※判定基準
⭐️: 超優良案件
⭐️⭐️: 良案件  
⭐️⭐️⭐️: 普通（要検討）
⭐️⭐️⭐️⭐️: 注意が必要
⭐️⭐️⭐️⭐️⭐️: 地雷案件（非推奨）
"""
                    
                    # テキストエリアで表示（コピーしやすい）
                    st.text_area(
                        "👇 このプロンプトをChatGPTまたはGeminiにコピペしてください",
                        value=prompt,
                        height=500,
                        key="prompt_phase1",
                        help="全選択してコピー（Ctrl+A → Ctrl+C）してください"
                    )
                    
                    st.success("✅ プロンプトを生成しました！")
                    
                    st.markdown("---")
                    st.markdown("**📋 次のステップ**")
                    st.markdown("""
                    1. 上記のテキストを全選択（Ctrl+A）してコピー（Ctrl+C）
                    2. [ChatGPT](https://chat.openai.com) または [Gemini](https://gemini.google.com) を開く
                    3. コピーしたテキストを貼り付けて送信
                    4. 分析結果が表示されます
                    
                    ※無料のChatGPT 3.5でも利用可能です
                    """)
    
    # フェーズ②: 契約後
    elif "② 契約後" in phase:
        st.header("② 契約後フェーズ: 指示の確認")
        st.markdown("**目的**: クライアントの真の意図を読み取り、修正リスクを事前回避")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 入力エリア")
            
            # 指示文入力
            instruction = st.text_area(
                "契約後の詳細指示をコピペ（必須）",
                height=200,
                placeholder="""例:
■調査対象: ペット用品、価格3,000円〜10,000円、50件
■必要情報: 商品名、価格、メーカー名、URL、評価
■注意点: 同メーカー3件まで、在庫切れ除外
■納期: 1週間以内""",
                help="クライアントから送られてきた具体的な作業指示を貼り付けてください"
            )
            
            # 不明点入力
            unclear_points = st.text_area(
                "不明点・気になる点（任意）",
                height=100,
                placeholder="例: 「テーマは自由」の範囲がわからない、納品形式が不明 など",
                help="指示で分からない部分や気になる点があれば入力してください"
            )
        
        with col2:
            st.subheader("🎨 生成されたプロンプト")
            
            if st.button("🔮 プロンプト生成", type="primary", use_container_width=True):
                if not instruction:
                    st.error("指示文を入力してください")
                else:
                    # プロンプト生成
                    prompt = f"""以下のクライアント指示を分析して、低単価ワーカーが「修正リスクを避けるため」の情報を提供してください。

【指示文】
{instruction}

【不明点・気になる点】
{unclear_points if unclear_points else "なし"}

以下の形式で出力してください：

---
## 🔍 指示解釈結果

### 1. 指示の要約
（クライアントが本当に求めているものを一言で）

### 2. 重要ポイント
- （絶対に守るべきポイント）
- （見落としがちなポイント）
- （優先順位が高い要素）

### 3. 曖昧な部分の解釈
- （「〜など」「適宜」などの曖昧表現の解釈）
- （明記されていないが期待されていること）

### 4. 地雷ポイント（修正リスク）
- （非承認や修正依頼につながりそうな落とし穴）
- （初心者が誤解しやすい部分）

### 5. 確認すべき質問
- （着手前にクライアントに確認すべきこと）
- （質問例文も提示）

### 6. 作業前チェックリスト
- [ ] （着手前に確認すべき項目）
- [ ] （準備すべきこと）
---
"""
                    
                    # テキストエリアで表示
                    st.text_area(
                        "👇 このプロンプトをChatGPTまたはGeminiにコピペしてください",
                        value=prompt,
                        height=500,
                        key="prompt_phase2",
                        help="全選択してコピー（Ctrl+A → Ctrl+C）してください"
                    )
                    
                    st.success("✅ プロンプトを生成しました！")
                    
                    st.markdown("---")
                    st.markdown("**📋 次のステップ**")
                    st.markdown("""
                    1. 上記のテキストを全選択（Ctrl+A）してコピー（Ctrl+C）
                    2. [ChatGPT](https://chat.openai.com) または [Gemini](https://gemini.google.com) を開く
                    3. コピーしたテキストを貼り付けて送信
                    4. 分析結果を確認して着手
                    
                    ※無料のChatGPT 3.5でも利用可能です
                    """)
    
    # フェーズ③: 執筆・納品
    elif "③ 執筆・納品" in phase:
        st.header("③ 執筆・納品フェーズ: 検品")
        st.markdown("**目的**: 納品前に自己チェックし、非承認・修正を防ぐ")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 入力エリア")
            
            # 指示文入力
            instruction_check = st.text_area(
                "元の指示文をコピペ（必須）",
                height=150,
                placeholder="クライアントから送られてきた指示文",
                help="元の指示内容を貼り付けてください"
            )
            
            # 納品物入力
            deliverable = st.text_area(
                "あなたの納品物をコピペ（必須）",
                height=300,
                placeholder="あなたが書いた文章や作成物を貼り付けてください",
                help="納品予定の文章や成果物を貼り付けてください"
            )
        
        with col2:
            st.subheader("🎨 生成されたプロンプト")
            
            if st.button("🔮 プロンプト生成", type="primary", use_container_width=True):
                if not instruction_check or not deliverable:
                    st.error("指示文と納品物の両方を入力してください")
                else:
                    # プロンプト生成
                    prompt = f"""以下の納品物を、クライアント指示と照らし合わせて「検品」してください。低単価ワーカーが「非承認・修正を避けるため」の情報を提供してください。

【元の指示文】
{instruction_check}

【納品物】
{deliverable}

以下の形式で出力してください：

---
## ✅ 検品結果

### 1. 総合評価（5段階）
⭐️⭐️⭐️⭐️⭐️ / ⭐️⭐️⭐️⭐️⭐️

### 2. 指示との一致度チェック
- [ ] 文字数・分量は適切か
- [ ] 指定されたテーマ・内容を満たしているか
- [ ] 禁止事項に触れていないか
- [ ] 納品形式は指示通りか

### 3. 品質チェック
- [ ] 誤字脱字はないか
- [ ] 文法・表現は自然か
- [ ] 読みやすさは十分か
- [ ] 情報の正確性は問題ないか

### 4. 修正が必要な箇所
**優先度：高**
- （このままだと非承認リスクがある箇所）

**優先度：中**
- （修正依頼が来そうな箇所）

**優先度：低**
- （あればより良い改善点）

### 5. 修正案
（具体的な修正文や改善提案）

### 6. 納品判定
【結果】✅ 納品OK / ⚠️ 要修正 / ❌ 作り直し推奨

### 7. コメント
（総合的なアドバイス）
---
"""
                    
                    # テキストエリアで表示
                    st.text_area(
                        "👇 このプロンプトをChatGPTまたはGeminiにコピペしてください",
                        value=prompt,
                        height=500,
                        key="prompt_phase3",
                        help="全選択してコピー（Ctrl+A → Ctrl+C）してください"
                    )
                    
                    st.success("✅ プロンプトを生成しました！")
                    
                    st.markdown("---")
                    st.markdown("**📋 次のステップ**")
                    st.markdown("""
                    1. 上記のテキストを全選択（Ctrl+A）してコピー（Ctrl+C）
                    2. [ChatGPT](https://chat.openai.com) または [Gemini](https://gemini.google.com) を開く
                    3. コピーしたテキストを貼り付けて送信
                    4. 検品結果を確認して修正・納品
                    
                    ※無料のChatGPT 3.5でも利用可能です
                    """)
    
    # フッター
    st.markdown("---")
    st.markdown("© 2024 ワーカー向け案件安全化ツール | 非承認・修正リスクを最小化")
