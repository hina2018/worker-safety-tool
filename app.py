import streamlit as st

st.set_page_config(
    page_title="AI活用クラウドワーク効率化ツール",
    page_icon="🚀",
    layout="wide"
)

# ─── パスワード認証 ───
PASSWORD = "worker2024"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 ログイン")
    pw = st.text_input("パスワードを入力してください", type="password")
    if st.button("ログイン"):
        if pw == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("パスワードが違います")
    st.stop()

# ─── カテゴリ定義 ───
CATEGORIES = {
    "① データ入力系": {
        "icon": "📊",
        "base_hourly": (200, 600),
        "ai_multiplier": 2.5,
        "description": "リスト作成・スプレッドシート入力・転記作業など",
        "tools": ["ChatGPT（整形・分類）", "Excel マクロ", "Google スプレッドシート 関数"],
        "steps": [
            "①案件の入力フォーマットを確認（5分）",
            "②ChatGPTで「一括変換プロンプト」を作成（10分）",
            "③サンプル10件で精度確認（5分）",
            "④残り全件を一括処理（人間は確認のみ）",
            "⑤最終目視チェック＆納品",
        ],
        "prompt_template": """以下のデータを指定フォーマットに変換してください。

【入力データ】
{input_data}

【変換ルール】
{rules}

【出力形式】
CSVで出力。1行目はヘッダー。文字コードUTF-8。

余計な説明は不要。変換結果のみ出力してください。""",
        "tips": [
            "同じパターンの繰り返し作業はChatGPTで1プロンプト化",
            "Excelの「フラッシュ入力」で規則性のある転記を自動化",
            "フォーマット確認は最初に徹底→後戻りゼロが最速",
        ],
        "next_step": "データ整形・クレンジング案件（時給400〜800円）へステップアップ",
    },
    "② 文字起こし系": {
        "icon": "🎙️",
        "base_hourly": (200, 600),
        "ai_multiplier": 3.0,
        "description": "音声・動画の文字起こし、講演録・会議録作成など",
        "tools": ["Whisper（OpenAI）", "notta", "Google Speech-to-Text"],
        "steps": [
            "①音声をWhisper/notta等のAIで自動文字起こし（精度85〜90%）",
            "②生成テキストをChatGPTで整形・誤字修正",
            "③人間が聞き取り困難箇所のみ手動修正",
            "④要求フォーマットに整形して納品",
        ],
        "prompt_template": """以下の文字起こしテキストを整形してください。

【元テキスト】
{raw_text}

【整形ルール】
・フィラー（えー、あのー等）を削除
・話者が変わるたびに改行
・句読点を適切に追加
・明らかな誤変換を修正

整形後のテキストのみ出力してください。""",
        "tips": [
            "Whisperは無料で精度90%超。まずAI任せで時短",
            "専門用語が多い案件は事前に用語リストをChatGPTに渡す",
            "1時間の音声→AI処理15分＋人間確認30分が現実的",
        ],
        "next_step": "議事録作成・要約付き文字起こし（時給600〜1,000円）へステップアップ",
    },
    "③ ライティング系": {
        "icon": "✍️",
        "base_hourly": (300, 1500),
        "ai_multiplier": 2.5,
        "description": "記事・ブログ・商品説明・SNS投稿文など",
        "tools": ["ChatGPT（構成・下書き）", "Grammarly（校正）", "コピペチェックツール"],
        "steps": [
            "①指示書からキーワード・要件を抽出（5分）",
            "②ChatGPTで構成案を作成→クライアント承認前に頭の中で確認（10分）",
            "③セクションごとにChatGPTで下書き生成（15分）",
            "④人間がトーン・事実確認・独自性を加筆編集（20分）",
            "⑤コピペチェック＆Grammarly校正→納品",
        ],
        "prompt_template": """以下の条件でブログ記事の下書きを作成してください。

【テーマ】{theme}
【ターゲット読者】{target}
【文字数】{word_count}文字
【キーワード】{keywords}
【トーン】{tone}

【構成】
H2見出し3〜5個で構成。
各H2の下にH3を2〜3個。
導入・本文・まとめの流れを守る。

下書きのみ出力。補足説明は不要。""",
        "tips": [
            "構成だけAIに作らせ、執筆は自分→品質保ちながら時短",
            "同ジャンル案件はプロンプトをテンプレ化→2件目から半分の時間",
            "コピペ率はAI生成のまま提出せず必ず人間で書き換え",
        ],
        "next_step": "SEO専門ライター・特化ジャンルライター（時給1,000〜2,000円）へステップアップ",
    },
    "④ リサーチ・リスト作成系": {
        "icon": "🔍",
        "base_hourly": (300, 800),
        "ai_multiplier": 2.0,
        "description": "競合調査・企業リスト作成・情報収集・まとめ作業など",
        "tools": ["ChatGPT（分析・要約）", "Perplexity（リサーチ）", "Notion（整理）"],
        "steps": [
            "①調査対象と要件を明確化（5分）",
            "②Perplexity/ChatGPTで大枠リサーチ（20分）",
            "③結果をChatGPTで表形式に整理・重複削除",
            "④人間が精度確認・一次ソース確認（15分）",
            "⑤フォーマット整形して納品",
        ],
        "prompt_template": """以下の条件でリサーチ結果を整理してください。

【調査対象】{target}
【必要な情報項目】{items}
【件数】{count}件

表形式（Markdown）で出力。
各項目は簡潔に。情報が不明な場合は「要確認」と記載。
余計な説明不要。表のみ出力。""",
        "tips": [
            "Perplexityは出典付きで情報収集→信頼性確認が速い",
            "リスト作成は件数単価が多い→1件あたりの時間を極限まで短縮",
            "ChatGPTに「重複を除いてCSVで出力」を指示→Excel加工不要",
        ],
        "next_step": "市場調査レポート・競合分析（時給1,000〜2,000円）へステップアップ",
    },
    "⑤ SNS運用系": {
        "icon": "📱",
        "base_hourly": (500, 1500),
        "ai_multiplier": 2.0,
        "description": "投稿文作成・スケジュール管理・コメント返信文案など",
        "tools": ["ChatGPT（投稿文生成）", "Buffer（スケジュール）", "Canva（画像）"],
        "steps": [
            "①クライアントのトンマナ・過去投稿を把握（初回30分）",
            "②月間投稿カレンダーをChatGPTで一括作成（20分）",
            "③各投稿文をChatGPTで下書き→人間がブランド調整（30分/月）",
            "④Canvaでテンプレ画像を量産",
            "⑤Bufferで予約投稿→完了",
        ],
        "prompt_template": """以下の条件でSNS投稿文を{count}件作成してください。

【アカウント情報】
・業種：{industry}
・ターゲット：{target}
・トーン：{tone}

【テーマ一覧】
{themes}

各投稿：
・本文（140文字以内）
・ハッシュタグ（5個以内）
・絵文字を適度に使用

番号付きリストで出力。""",
        "tips": [
            "トンマナを最初にChatGPTに覚えさせれば毎回説明不要",
            "月30投稿を月2時間で管理が目標",
            "画像テンプレをCanvaで10種類作れば使い回し可能",
        ],
        "next_step": "SNSコンサルタント・アカウント運用代行（月額5万〜15万円）へステップアップ",
    },
    "⑥ 翻訳・多言語系": {
        "icon": "🌐",
        "base_hourly": (400, 1200),
        "ai_multiplier": 2.5,
        "description": "英日・日英翻訳、多言語コンテンツ作成など",
        "tools": ["DeepL（高精度翻訳）", "ChatGPT（文脈調整）", "DeepL Write（校正）"],
        "steps": [
            "①DeepLで全文を一次翻訳（時間の70%削減）",
            "②ChatGPTで専門用語・固有名詞を確認・修正",
            "③人間がニュアンス・文化的表現を調整",
            "④DeepL Writeで自然さを確認",
            "⑤用語統一チェック→納品",
        ],
        "prompt_template": """以下の翻訳文のニュアンスを確認・改善してください。

【原文（{source_lang}）】
{original}

【DeepL翻訳結果（{target_lang}）】
{deepl_result}

【改善指示】
・自然な表現に修正
・業界用語を適切な日本語に
・原文のトーンを維持

改善後の翻訳文のみ出力。""",
        "tips": [
            "DeepL翻訳→ChatGPT校正の2段階が品質と速度の最適解",
            "専門分野の用語集をChatGPTに渡せば一貫性が保たれる",
            "英日翻訳はDeepLの精度が高い。日→珍しい言語はChatGPT優位",
        ],
        "next_step": "専門分野翻訳（法律・医療・IT）（時給1,500〜3,000円）へステップアップ",
    },
    "⑦ 画像・動画編集補助系": {
        "icon": "🎬",
        "base_hourly": (500, 2000),
        "ai_multiplier": 2.0,
        "description": "動画の字幕付け・サムネイル作成・簡単な編集補助など",
        "tools": ["Captions.ai（字幕）", "Canva（サムネイル）", "CapCut（動画編集）"],
        "steps": [
            "①動画をCaptions.aiで自動字幕生成（精度90%）",
            "②ChatGPTで字幕テキストの誤字修正・タイミング調整",
            "③Canvaテンプレでサムネイル量産（1枚10分）",
            "④CapCutの自動カット機能で無音部分を削除",
            "⑤最終確認→納品",
        ],
        "prompt_template": """以下の動画字幕の誤字・不自然な表現を修正してください。

【字幕テキスト（SRT形式）】
{srt_content}

【修正指示】
・明らかな誤変換を修正
・話し言葉を適度に整える（でも自然さは残す）
・句読点を調整

修正後のSRT形式で出力。タイムコードは変更しない。""",
        "tips": [
            "字幕付けはCaptions.aiで90%自動化→手修正は最小限",
            "サムネイルはCanvaの同一テンプレを使い回す→ブランド統一も同時達成",
            "CapCutの自動機能を使いこなせば編集時間が半分以下に",
        ],
        "next_step": "動画編集・YouTubeチャンネル運用代行（時給1,500〜3,000円）へステップアップ",
    },
    "⑧ 簡単なWeb制作系": {
        "icon": "💻",
        "base_hourly": (800, 2500),
        "ai_multiplier": 2.0,
        "description": "LP・コーポレートサイト制作、WordPressカスタマイズなど",
        "tools": ["ChatGPT（コード生成）", "GitHub Copilot", "WordPress"],
        "steps": [
            "①要件定義をChatGPTで整理・仕様書化（30分）",
            "②ChatGPTにデザイン要件を渡してHTML/CSS下書き生成",
            "③人間がデザイン確認・ブランド調整・レスポンシブ確認",
            "④ChatGPTでバグ修正・最適化",
            "⑤クロスブラウザ確認→納品",
        ],
        "prompt_template": """以下の要件でHTMLランディングページのコードを作成してください。

【要件】
・業種：{industry}
・目的：{purpose}
・必須セクション：{sections}
・カラー：{colors}
・フォント：{fonts}

【技術要件】
・HTML5 / CSS3
・レスポンシブ対応（Bootstrap5使用可）
・JavaScript最小限

完全なHTMLファイルとして出力。""",
        "tips": [
            "ChatGPTはコード生成が得意→指示が具体的なほど精度UP",
            "デザインはFigmaのフリーテンプレをベースに→ゼロから作らない",
            "WordPress案件はElementorで大半がノーコード対応可能",
        ],
        "next_step": "Webデザイナー・フロントエンド開発（時給2,000〜5,000円）へステップアップ",
    },
}

# ─── UI ───
st.title("🚀 AI活用クラウドワーク効率化ツール")
st.caption("同じ作業をAIで効率化 → 時給2〜3倍を目指す")

st.divider()

# ─── カテゴリ選択 ───
cat_names = list(CATEGORIES.keys())
selected = st.selectbox(
    "📂 作業カテゴリを選択してください",
    cat_names,
    format_func=lambda x: f"{CATEGORIES[x]['icon']} {x}"
)

cat = CATEGORIES[selected]

# ─── 案件情報入力 ───
st.subheader(f"{cat['icon']} {selected}")
st.caption(cat["description"])

col1, col2 = st.columns(2)

with col1:
    job_title = st.text_input("📋 案件タイトル（任意）", placeholder="例：商品データ入力100件")
    job_description = st.text_area("📄 募集文・指示書（貼り付け）", height=180,
                                    placeholder="クラウドワークスやランサーズの案件文をそのまま貼り付けてください")

with col2:
    reward = st.number_input("💴 報酬（円）", min_value=0, value=1000, step=100)
    est_hours = st.number_input("⏱️ 通常作業時間の見積もり（時間）", min_value=0.5, value=2.0, step=0.5)
    ai_experience = st.selectbox("🤖 AI活用経験", ["初めて", "少しある（ChatGPT使ったことある）", "慣れている"])

# ─── 分析実行 ───
if st.button("⚡ AI効率化プランを生成", type="primary", use_container_width=True):

    # 時給計算
    base_hourly = reward / est_hours if est_hours > 0 else 0
    ai_hours = est_hours / cat["ai_multiplier"]
    ai_hourly = reward / ai_hours if ai_hours > 0 else 0

    st.divider()
    st.subheader("📊 効率化プラン")

    # ─── 時給メーター ───
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("現状の推定時給", f"¥{int(base_hourly):,}/時間")
    with col_b:
        st.metric(
            "AI活用後の推定時給",
            f"¥{int(ai_hourly):,}/時間",
            delta=f"+¥{int(ai_hourly - base_hourly):,}（{cat['ai_multiplier']}倍）"
        )
    with col_c:
        st.metric("削減できる作業時間", f"{est_hours - ai_hours:.1f}時間削減",
                  delta=f"{int((1 - 1/cat['ai_multiplier'])*100)}%カット")

    # ─── 相場比較 ───
    lo, hi = cat["base_hourly"]
    st.info(
        f"📌 **{selected}の相場時給：¥{lo:,}〜¥{hi:,}/時間**\n\n"
        f"現状時給 ¥{int(base_hourly):,} → AI活用後 ¥{int(ai_hourly):,}（相場{'内' if lo <= ai_hourly <= hi else '上' if ai_hourly > hi else '下'}）"
    )

    # ─── 作業手順 ───
    st.subheader("⚙️ AI活用の最短作業手順")
    for step in cat["steps"]:
        st.write(f"• {step}")

    # ─── 使用ツール ───
    st.subheader("🛠️ 使用するAIツール")
    cols = st.columns(len(cat["tools"]))
    for i, tool in enumerate(cat["tools"]):
        cols[i].success(tool)

    # ─── 時短テクニック ───
    st.subheader("💡 時短テクニック")
    for tip in cat["tips"]:
        st.write(f"✅ {tip}")

    # ─── プロンプトテンプレート ───
    with st.expander("📋 AIプロンプトテンプレート（コピーして使用）"):
        st.code(cat["prompt_template"], language="text")

    # ─── ステップアップ戦略 ───
    st.subheader("🎯 次のステップ（時給UPの道筋）")
    st.success(f"🚀 {cat['next_step']}")

    # ─── AI利用の注意事項 ───
    st.divider()
    with st.expander("⚠️ AI活用時の注意事項（必読）"):
        st.warning(
            "**プラットフォームのルールを必ず確認**\n\n"
            "・AI使用可否は案件ごとに異なります。募集文や依頼主に確認してください。\n"
            "・納品物の最終チェックは必ず人間が行ってください。\n"
            "・AI生成コンテンツの事実確認は必須です。\n"
            "・クオリティを保つことが長期的な信頼・単価UPにつながります。"
        )

# ─── サイドバー：ステップアップロードマップ ───
with st.sidebar:
    st.header("📈 時給UPロードマップ")
    st.write("**初心者（時給100〜300円）**")
    st.caption("データ入力・文字起こし・タスク")
    st.write("↓ AI効率化で作業時間1/3")
    st.write("**中級者（時給400〜800円）**")
    st.caption("ライティング・リサーチ・SNS")
    st.write("↓ 専門性・実績を積む")
    st.write("**上級者（時給1,000〜3,000円）**")
    st.caption("専門ライター・翻訳・Web制作")
    st.write("↓ 継続案件・直接契約")
    st.write("**フリーランサー（月収15万〜）**")
    st.caption("継続クライアント・単価交渉")

    st.divider()
    st.header("🤖 推奨AIツール（無料）")
    st.write("• **ChatGPT** - 万能AI")
    st.write("• **Perplexity** - リサーチ")
    st.write("• **DeepL** - 翻訳")
    st.write("• **Whisper** - 文字起こし")
    st.write("• **Canva** - デザイン")
    st.write("• **CapCut** - 動画編集")
