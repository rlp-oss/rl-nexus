import streamlit as st
import base64
import json
import urllib.parse

# --- CONFIG & STYLING ---
st.set_page_config(page_title="RL Nexus", page_icon="🔗", layout="centered")

# Custom CSS for the "Card" look
st.markdown("""
<style>
    .profile-img {
        border-radius: 50%;
        border: 4px solid #FFD700;
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 120px;
    }
    .user-name {
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: 700;
        font-size: 2em;
        margin-bottom: 0px;
    }
    .user-bio {
        text-align: center;
        font-style: italic;
        color: #888;
        margin-top: -10px;
    }
    .stButton button {
        width: 100%;
        border-radius: 25px;
        height: 55px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton button:hover {
        transform: scale(1.02);
        border-color: #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def encode_data(data):
    """Turns the dictionary into a URL-safe string"""
    json_str = json.dumps(data)
    return base64.urlsafe_b64encode(json_str.encode()).decode()

def decode_data(token):
    """Turns the URL string back into a dictionary"""
    try:
        json_str = base64.urlsafe_b64decode(token.encode()).decode()
        return json.loads(json_str)
    except:
        return None

# --- MAIN APP LOGIC ---

# 1. CHECK URL FOR DATA (VIEW MODE)
query_params = st.query_params
if "hub" in query_params:
    # --- VIEWER MODE ---
    data = decode_data(query_params["hub"])
    
    if data:
        # Render the Profile
        st.markdown(f'<img src="{data["image"]}" class="profile-img">', unsafe_allow_html=True)
        st.markdown(f'<p class="user-name">{data["name"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="user-bio">{data["bio"]}</p>', unsafe_allow_html=True)
        st.write("---")
        
        # Render the Links
        for link in data["links"]:
            st.link_button(label=link["label"], url=link["url"], use_container_width=True)
            
        st.write("---")
        if st.button("⚡ Create Your Own Nexus Hub"):
            st.query_params.clear()
            st.rerun()
            
    else:
        st.error("Invalid Nexus Link. The data might be corrupted.")

else:
    # --- BUILDER MODE ---
    st.title("🔗 RL Nexus")
    st.subheader("The Social Link Hub")
    st.info("Build your Hub. Share one link. Discover others.")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        name = st.text_input("Display Name", value="C.W. Germain")
        bio = st.text_area("Mini Bio", value="Founder of Rhythm Logic & BubbleBum Books")
        image_url = st.text_input("Profile Image URL", value="https://media.licdn.com/dms/image/v2/D5603AQF4g6bXlF3XwQ/profile-displayphoto-shrink_800_800/0/1705175000000?e=2147483647&v=beta&t=XXXX")
        
    with col2:
        st.write("### Your Links")
        links = []
        
        # We'll default 4 slots for now
        l1_label = st.text_input("Link 1 Label", "LinkedIn Profile")
        l1_url = st.text_input("Link 1 URL", "https://www.linkedin.com/in/c-w-germain-6507903a5/")
        
        l2_label = st.text_input("Link 2 Label", "BubbleBum Books")
        l2_url = st.text_input("Link 2 URL", "https://bubblebumbooks.com")
        
        l3_label = st.text_input("Link 3 Label", "Rhythm Logic Publishing")
        l3_url = st.text_input("Link 3 URL", "https://rhythmlogicpublishing.com")
        
        l4_label = st.text_input("Link 4 Label", "YouTube Channel")
        l4_url = st.text_input("Link 4 URL", "https://youtube.com/@rhythmlogicpublishing")

        if l1_url: links.append({"label": l1_label, "url": l1_url})
        if l2_url: links.append({"label": l2_label, "url": l2_url})
        if l3_url: links.append({"label": l3_label, "url": l3_url})
        if l4_url: links.append({"label": l4_label, "url": l4_url})

    # GENERATE BUTTON
    if st.button("🚀 Generate My Nexus Link"):
        user_data = {
            "name": name,
            "bio": bio,
            "image": image_url,
            "links": links
        }
        token = encode_data(user_data)
        
        # Get base URL (Localhost or Streamlit Cloud)
        base_url = "https://voice-logic-....streamlit.app" # <--- REPLACE THIS WITH YOUR APP URL ONCE DEPLOYED
        final_link = f"{base_url}/?hub={token}"
        
        st.success("Hub Created! Here is your magic link:")
        st.code(final_link, language="text")
        st.caption("Copy this link and put it in your Facebook/LinkedIn Bio. It will permanently show your Hub.")
        
        # Preview
        st.divider()
        st.write("### Preview:")
        st.markdown(f'<img src="{image_url}" class="profile-img">', unsafe_allow_html=True)
        st.markdown(f'<p class="user-name">{name}</p>', unsafe_allow_html=True)
        for link in links:
            st.button(link["label"], key=link["url"], use_container_width=True)

    st.write("---")
    st.markdown("### 🌎 Community Stream (Mockup)")
    st.caption("In the future, this section will show other trending Hubs.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Hubs", "12")
    c2.metric("Total Links", "48")
    c3.metric("Clicks Today", "154")