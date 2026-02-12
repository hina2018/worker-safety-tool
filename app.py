import streamlit as st
import json

# ページ設定
st.set_page_config(
    page_title="ワーカー向け案件安全化ツール",
    page_icon="🛡️",
    layout="wide"
)

# ======================
# パスワード認証
# ======================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🛡️ ワーカー向け案件安全化ツール")
    st.markdown("---")
    st.markdown("### 🔐 ログイン")
    st.markdown("購入時にお伝えしたパスワードを入力してください")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("パスワード", type="password", key="password_input")
        
        if st.button("ログイン", type="primary", use_container_width=True):
            # パスワードチェック（購入者ごとに変更可能）
            if password == "worker2024":  # ← ここを購入者ごとに変更
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ パスワードが正しくありません")
        
        st.markdown("---")
        st.info("💡 パスワードを忘れた場合は、購入時のメールをご確認ください")
    
    st.stop()

# ======================
# ログイン後のメイン画面
# ======================

# カスタムCSS
st.markdown("""
<style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .danger {
        background-color: #ffebee;
        padding: 15px;
        border-left: 5px solid #f44336;
        margin: 10px 0;
    }
    .warning {
        background-color: #fff3e0;
        padding: 15px;
        border-left: 5px solid #ff9800;
        margin: 10px 0;
    }
    .safe {
        background-color: #e8f5e9;
        padding: 15px;
        border-left: 5px solid #4caf50;
        margin: 10px 0;
    }
    .prompt-box {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 5px;
        margin: 15px 0;
        font-family: monospace;
        white-space: pre-wrap;
        border: 2px solid #2196F3;
    }
    .copy-button {
        background-color: #2196F3;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .instruction-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

# タイトル
st.title("🛡️ ワーカー向け案件安全化ツール")
st.markdown("**コンセプト**: 案件選びから納品まで、非承認・修正リスクを最小化")

# ログアウトボタン
if st.button("🚪 ログアウト", key="logout_btn"):
    st.session_state.logged_in = False
    st.rerun()

st.markdown("---")

# セッション状態の初期化
if 'phase' not in st.session_state:
    st.session_state.phase = 1

# サイドバー：フェーズ選択
st.sidebar.title("📋 作業フェーズ")
phase = st.sidebar.radio(
    "現在のフェーズを選択:",
    ["① 案件探し（時給・地雷判定）", "② 着手前（指示解釈）", "③ 執筆・納品（検品）"],
    index=st.session_state.phase - 1
)

# フェーズ番号を取得
if "①" in phase:
    st.session_state.phase = 1
elif "②" in phase:
    st.session_state.phase = 2
elif "③" in phase:
    st.session_state.phase = 3

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 使い方")
st.sidebar.markdown("""
1. 情報を入力
2. プロンプト生成ボタンをクリック
3. 表示されたプロンプトをコピー
4. ChatGPTまたはGeminiに貼り付け
5. 結果を確認して判断
""")

# 典型的な案件例（サンプルデータ）
SAMPLE_JOB = """【募集内容】
美容関連の記事作成
文字数：3000文字以上
報酬：1記事500円
納期：受注後3日以内

【記事テーマ例】
・30代女性向けスキンケア方法
・敏感肌向けおすすめ化粧品
・季節別美容ケアのポイント

【注意事項】
・オリジナル文章必須（コピペ厳禁）
・読みやすい文章でお願いします
・専門的すぎない、親しみやすい文体で
・NGワード：「絶対」「必ず」「効果抜群」など断定表現
"""

SAMPLE_APPROVED = """30代からのスキンケアで大切なのは、保湿と紫外線対策です。

年齢を重ねると、お肌の水分量が減少しやすくなります。そのため、化粧水でたっぷり水分を与えた後、乳液やクリームでしっかり蓋をすることが重要です。

また、紫外線は肌老化の大きな原因の一つと言われています。曇りの日でも日焼け止めを塗る習慣をつけると、将来のお肌の状態が変わってくるかもしれません。

さらに、クレンジングも見直してみましょう。ゴシゴシ洗いは避けて、優しく丁寧に汚れを落とすことで、肌への負担を減らせます。

毎日のちょっとした心がけが、5年後、10年後のお肌を作ります。
"""

# ======================
# フェーズ1: 案件探し
# ======================
if st.session_state.phase == 1:
    st.header("① 案件探しフェーズ：時給・地雷判定")
    st.markdown("**目的**: 損な案件をスルーし、「勝てる案件」だけに集中")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 入力エリア")
        
        job_text = st.text_area(
            "募集文をコピペ（必須）",
            height=250,
            placeholder=SAMPLE_JOB,
            help="クラウドソーシングサイトの募集文をそのまま貼り付けてください"
        )
        
        genre = st.selectbox(
            "ジャンル（任意）",
            ["指定なし", "美容・健康", "金融・投資", "不動産", "転職・キャリア", "育児・子育て", "IT・テクノロジー", "その他"]
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            work_speed = st.selectbox(
                "あなたの作業スピード",
                ["普通", "速い", "遅い"]
            )
        with col_b:
            target_hourly = st.number_input(
                "希望時給（円）",
                min_value=500,
                max_value=5000,
                value=1500,
                step=100
            )
        
        if st.button("🔍 プロンプト生成", type="primary", key="phase1_gen"):
            if not job_text:
                st.error("募集文を入力してください")
            else:
                st.session_state.phase1_prompt = True
    
    with col2:
        st.subheader("📤 生成されたプロンプト")
        
        if 'phase1_prompt' in st.session_state and st.session_state.phase1_prompt:
            
            # プロンプト生成
            prompt = f"""以下の案件募集文を分析して、低単価ワーカー向けに「受注すべきか判断する情報」を提供してください。

【募集文】
{job_text}

【あなたの情報】
- 作業スピード: {work_speed}
- 希望時給: {target_hourly}円
- ジャンル: {genre if genre != "指定なし" else "なし"}

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
            
            st.markdown('<div class="instruction-box">👇 このプロンプトをChatGPTまたはGeminiにコピペしてください</div>', unsafe_allow_html=True)
            
            st.code(prompt, language=None)
            
            if st.button("📋 プロンプトをクリップボードにコピー", key="copy1"):
                st.write("✅ コピーしました！（手動でコピーしてください）")
            
            st.markdown("---")
            st.markdown("### 💬 AI の回答を貼り付け（任意）")
            ai_response = st.text_area(
                "ChatGPT/Geminiの回答をここに貼り付けると記録できます",
                height=200,
                key="phase1_response"
            )
            
            if ai_response:
                st.success("✅ 回答を記録しました")

# ======================
# フェーズ2: 着手前（指示解釈）
# ======================
elif st.session_state.phase == 2:
    st.header("② 着手前フェーズ：曖昧指示→3パターン安全解釈")
    st.markdown("**目的**: 指示の解釈に悩む時間をゼロに")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 入力エリア")
        
        job_text2 = st.text_area(
            "募集文をコピペ（必須）",
            height=200,
            placeholder=SAMPLE_JOB,
            help="案件の募集文を貼り付け"
        )
        
        approved_texts = st.text_area(
            "過去承認文（任意、1〜3件）",
            height=150,
            placeholder=SAMPLE_APPROVED,
            help="過去に承認された文章があれば貼り付け"
        )
        
        manual_text = st.text_area(
            "マニュアル・禁止事項（任意）",
            height=100,
            placeholder="例: 断定表現禁止、「〜です・ます」調統一、改行は2行ごと"
        )
        
        other_jobs = st.text_area(
            "クライアントの他案件指示文（任意）",
            height=100,
            placeholder="同じクライアントの別案件があれば参考に"
        )
        
        concern = st.text_area(
            "不安点コメント（任意）",
            height=80,
            placeholder="例: 「読みやすい文章」が具体的にどういう意味か不明"
        )
        
        if st.button("🔍 プロンプト生成", type="primary", key="phase2_gen"):
            if not job_text2:
                st.error("募集文を入力してください")
            else:
                st.session_state.phase2_prompt = True
    
    with col2:
        st.subheader("📤 生成されたプロンプト")
        
        if 'phase2_prompt' in st.session_state and st.session_state.phase2_prompt:
            
            # プロンプト生成
            prompt = f"""以下の案件募集文の「曖昧な指示」を、3つの安全な解釈パターンに分けて提案してください。

【募集文】
{job_text2}

【過去承認文】
{approved_texts if approved_texts else "なし"}

【マニュアル・禁止事項】
{manual_text if manual_text else "なし"}

【クライアントの他案件指示文】
{other_jobs if other_jobs else "なし"}

【ワーカーの不安点】
{concern if concern else "なし"}

以下の形式で出力してください：

---
## 📋 指示解釈の3パターン提案

### パターンA：質重視（詳細・丁寧）
**解釈内容:**
- （具体的にどう書くか）
- （文字数、構成、トーンなど）

**想定される評価:**
- メリット: 
- デメリット:
- 修正リスク: 低/中/高

---

### パターンB：量重視（多く・効率重視）
**解釈内容:**
- （具体的にどう書くか）

**想定される評価:**
- メリット:
- デメリット:
- 修正リスク: 低/中/高

---

### パターンC：スピード重視（簡潔・即納）
**解釈内容:**
- （具体的にどう書くか）

**想定される評価:**
- メリット:
- デメリット:
- 修正リスク: 低/中/高

---

## ✅ 推奨解釈
**パターン○を推奨**

**理由:**
- （なぜこのパターンが最も安全か）
- （過去承認文やマニュアルとの整合性）
- （修正されにくい理由）

## ⚠️ 注意点リスト
1. （マニュアル違反になりやすいポイント）
2. （NG表現の具体例）
3. （クライアントが嫌がりそうな書き方）

---
"""
            
            st.markdown('<div class="instruction-box">👇 このプロンプトをChatGPTまたはGeminiにコピペしてください</div>', unsafe_allow_html=True)
            
            st.code(prompt, language=None)
            
            if st.button("📋 プロンプトをクリップボードにコピー", key="copy2"):
                st.write("✅ コピーしました！（手動でコピーしてください）")
            
            st.markdown("---")
            st.markdown("### 💬 AI の回答を貼り付け（任意）")
            ai_response2 = st.text_area(
                "ChatGPT/Geminiの回答をここに貼り付けると記録できます",
                height=200,
                key="phase2_response"
            )
            
            if ai_response2:
                st.success("✅ 回答を記録しました")

# ======================
# フェーズ3: 執筆・納品（検品）
# ======================
elif st.session_state.phase == 3:
    st.header("③ 執筆・納品フェーズ：合格文体再現＆検品")
    st.markdown("**目的**: 非承認を物理的に阻止、継続案件につなげる")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 入力エリア")
        
        draft_text = st.text_area(
            "今回の下書き文章（必須）",
            height=250,
            placeholder="あなたが書いた下書き文章を貼り付けてください"
        )
        
        approved_text3 = st.text_area(
            "過去承認文（必須、1件以上）",
            height=150,
            placeholder=SAMPLE_APPROVED,
            help="このクライアントで承認された過去の文章"
        )
        
        manual_text3 = st.text_area(
            "マニュアル・禁止事項（任意）",
            height=100,
            placeholder="例: 断定表現禁止、改行ルール、NGワード"
        )
        
        if st.button("🔍 検品プロンプト生成", type="primary", key="phase3_gen"):
            if not draft_text:
                st.error("下書き文章を入力してください")
            elif not approved_text3:
                st.error("過去承認文を最低1件入力してください")
            else:
                st.session_state.phase3_prompt = True
    
    with col2:
        st.subheader("📤 生成されたプロンプト")
        
        if 'phase3_prompt' in st.session_state and st.session_state.phase3_prompt:
            
            # プロンプト生成
            prompt = f"""以下の下書き文章を、過去承認文の文体・ルールに合わせて修正し、NG表現を検出してください。

【今回の下書き文章】
{draft_text}

【過去承認文（お手本）】
{approved_text3}

【マニュアル・禁止事項】
{manual_text3 if manual_text3 else "なし"}

以下の形式で出力してください：

---
## ✅ 修正済み文章

（ここに修正後の文章を出力）

---

## 🔍 検出したNG表現

| 元の表現 | 問題点 | 修正案 |
|---------|--------|--------|
| 「○○」 | △△のため禁止 | 「××」に修正 |

---

## 📊 違反リスクスコア
⭐️⭐️⭐️ (1〜5段階)

**判定理由:**
- （過去承認文との文体一致度）
- （マニュアル遵守状況）
- （修正される可能性）

---

## 💡 修正アドバイス

### 文体の調整ポイント
1. （過去承認文と比べて改善した点）
2. （まだ調整の余地がある部分）

### 安全性を高めるコツ
- （このクライアントが好む表現パターン）
- （逆に嫌われやすい表現）

---

## ⚠️ 最終チェックリスト
- [ ] 文字数は基準を満たしているか
- [ ] 禁止表現は含まれていないか
- [ ] 過去承認文と文体が一致しているか
- [ ] 改行ルールは守られているか
- [ ] 誤字脱字はないか

---
"""
            
            st.markdown('<div class="instruction-box">👇 このプロンプトをChatGPTまたはGeminiにコピペしてください</div>', unsafe_allow_html=True)
            
            st.code(prompt, language=None)
            
            if st.button("📋 プロンプトをクリップボードにコピー", key="copy3"):
                st.write("✅ コピーしました！（手動でコピーしてください）")
            
            st.markdown("---")
            st.markdown("### 💬 AI の回答を貼り付け（任意）")
            ai_response3 = st.text_area(
                "ChatGPT/Geminiの回答をここに貼り付けると記録できます",
                height=250,
                key="phase3_response"
            )
            
            if ai_response3:
                st.success("✅ 回答を記録しました")
                st.markdown("### 📝 修正済み文章をコピーして納品できます")

# フッター
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 このツールはブラウザ完結型です。APIキー不要・課金なし・データ保存なし</p>
    <p>ChatGPT（無料版可）またはGemini（無料版可）で動作します</p>
</div>
""", unsafe_allow_html=True)
