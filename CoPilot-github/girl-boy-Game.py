import streamlit as st


st.set_page_config(page_title="GIRL OR BOY GAME", page_icon="🎲", layout="centered")
# Set page background to light pink
st.markdown("<style>body{background-color:#FFB6C1 !important;}</style>", unsafe_allow_html=True)
# Centered title in red
st.markdown("<h1 style='text-align: center; color: red;'>GIRL OR BOY GAME</h1>", unsafe_allow_html=True)

# Initialize session state
if 'started' not in st.session_state:
    st.session_state.started = False
    st.session_state.chosen_gender = None
    st.session_state.chosen_number = None

# Heart emojis
heart_emojis = ["❤️", "💙", "💚", "💛", "💜", "🧡", "🤍", "🤎", "💖", "💗", "💓", "💕", "💞", "💘", "💝", "💟", "❣️", "💌", "💋", "💍"]

# Characteristics for Boy
boy_characteristics = [
    "Handsome", "Brave", "Kind", "Funny", "Smart", "Helpful", "Honest", "Strong",
    "Caring", "Friendly", "Generous", "Loyal", "Respectful", "Adventurous", "Creative",
    "Patient", "Polite", "Talented", "Wise", "Ambitious"
]

# Characteristics for Girl
girl_characteristics = [
    "Beautiful", "Sweet", "Gentle", "Cheerful", "Intelligent", "Compassionate", "Trustworthy", "Graceful",
    "Loving", "Sociable", "Thoughtful", "Faithful", "Courteous", "Daring", "Artistic",
    "Calm", "Well-mannered", "Gifted", "Knowledgeable", "Determined"
]

boy_chars = dict(zip(heart_emojis, boy_characteristics))
girl_chars = dict(zip(heart_emojis, girl_characteristics))

# Set kid-friendly background color and button styles
st.markdown("""
<style>

.stButton button {
    font-size: 32px !important;
    padding: 20px 40px !important;
    color: green !important;
    border-radius: 25px !important;
            background: #FFD700 !important;  /* Gold */
}
.start-btn button {
    background: #FFD700 !important;  /* Gold */
}
.girl-btn button {
    background: #FF69B4 !important;  /* Pink */
}
.boy-btn button {
    background: #4169E1 !important;  /* Blue */
}
.num-1 button { background: #FF0000 !important; }
.num-2 button { background: #0000FF !important; }
.num-3 button { background: #00FF00 !important; }
.num-4 button { background: #FFFF00 !important; }
.num-5 button { background: #800080 !important; }
.num-6 button { background: #FFA500 !important; }
.num-7 button { background: #FFC0CB !important; }
.num-8 button { background: #A52A2A !important; }
.num-9 button { background: #808080 !important; }
.num-10 button { background: #00FFFF !important; }
.num-11 button { background: #FF00FF !important; }
.num-12 button { background: #00FF7F !important; }
.num-13 button { background: #008080 !important; }
.num-14 button { background: #000080 !important; }
.num-15 button { background: #800000 !important; }
.num-16 button { background: #808000 !important; }
.num-17 button { background: #C0C0C0 !important; }
.num-18 button { background: #000000 !important; }
.num-19 button { background: #FFFFFF !important; color: black !important; }
.num-20 button { background: #FFD700 !important; }
.heart-1 button { background: #FF0000 !important; }
.heart-2 button { background: #0000FF !important; }
.heart-3 button { background: #00FF00 !important; }
.heart-4 button { background: #FFFF00 !important; }
.heart-5 button { background: #800080 !important; }
.heart-6 button { background: #FFA500 !important; }
.heart-7 button { background: #FFC0CB !important; }
.heart-8 button { background: #A52A2A !important; }
.heart-9 button { background: #808080 !important; }
.heart-10 button { background: #00FFFF !important; }
.heart-11 button { background: #FF00FF !important; }
.heart-12 button { background: #00FF7F !important; }
.heart-13 button { background: #008080 !important; }
.heart-14 button { background: #000080 !important; }
.heart-15 button { background: #800000 !important; }
.heart-16 button { background: #808000 !important; }
.heart-17 button { background: #C0C0C0 !important; }
.heart-18 button { background: #000000 !important; }
.heart-19 button { background: #FFFFFF !important; color: black !important; }
.heart-20 button { background: #FFD700 !important; }
</style>
""", unsafe_allow_html=True)

# Dialog function
@st.dialog(f"Your are a {st.session_state.chosen_gender} With a Heart Number {st.session_state.chosen_number}")
def show_characteristic(gender, number, emoji, char):
    st.write(f"{emoji} => {char}")
    if st.button("Play Again"):
        st.session_state.started = False
        st.session_state.chosen_gender = None
        st.session_state.chosen_number = None
        st.rerun()

# Start screen - centered
if not st.session_state.started:
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown('<div class="start-btn">', unsafe_allow_html=True)
        if st.button("Start"):
            st.session_state.started = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # Gender selection - hide after chosen
    if not st.session_state.chosen_gender:
        col1, col2 = st.columns([15,0.2])  # Move buttons to left/center
        with col1:
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                st.markdown('<div class="girl-btn">', unsafe_allow_html=True)
                if st.button("Girl"):
                    st.session_state.chosen_gender = "Girl"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with sub_col2:
                st.markdown('<div class="boy-btn">', unsafe_allow_html=True)
                if st.button("Boy"):
                    st.session_state.chosen_gender = "Boy"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.write("")  # Empty for spacing

    # Number selection expander - hide after chosen
    if st.session_state.chosen_gender and not st.session_state.chosen_number:
        st.write(f"You chose :red[{st.session_state.chosen_gender}]")
        cols = st.columns(5)
        for i in range(1, 21):
            st.markdown(f'<div class="num-{i}">', unsafe_allow_html=True)
            if cols[(i-1) % 5].button(str(i)):
                st.session_state.chosen_number = i
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)    

    # Hearts expander - show after number chosen
    if st.session_state.chosen_number:
        st.write(f"You chose number {st.session_state.chosen_number}")
        chars = boy_chars if st.session_state.chosen_gender == "Boy" else girl_chars
        i = st.session_state.chosen_number
        emoji = heart_emojis[i-1]
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
                st.markdown(f'<div class="heart-{i}">', unsafe_allow_html=True)
                if st.button(f"{emoji} {i}"):
                    show_characteristic(st.session_state.chosen_gender, st.session_state.chosen_number, emoji, chars[emoji])
                st.markdown('</div>', unsafe_allow_html=True)
