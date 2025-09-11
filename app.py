import streamlit as st
from modules import introduction, step1, step2, step3, step4

# Page configuration
st.set_page_config(
    page_title="Demo Pipeline",
    page_icon="😎",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    st.title("🚀 Demo Pipeline")
    # Sidebar
    st.sidebar.title("📋 Navigation")
    
    # Project selector
    project = st.sidebar.selectbox("🎯 Project:", ["Student Performance Analysis", "Retail Data Analytics"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📍 Pipeline Steps")
    
    # Options including Introduction
    options = [
        "🏠 Introduction",
        "🔧 Step 1: Data Quality Assessment", 
        "⚙️ Step 2: Metadata Extraction",
        "🔍 Step 3: Transformation to RPCM Entities",
        "📈 Step 4: Taxonomy Queries"
    ]
    
    # Single selectbox
    selected_step = st.sidebar.selectbox(
        "Select step:",
        options,
        index=0  # Default to "Introduction"
    )
    
    # --- Progress Tracker ---
    total_steps = len(options) - 1  # quitamos "Introduction"
    current_step = options.index(selected_step)
    progress = current_step / total_steps if current_step > 0 else 0
    
    st.progress(progress)
    if current_step == 0:
        st.caption("📌 Currently at: Introduction")
    else:
        st.caption(f"📌 Step {current_step} of {total_steps}")
    
    # --- Main content ---
    if selected_step == "🏠 Introduction":
        introduction.show(project)
    else:
        show_content(selected_step, project)

def show_content(section, project):
    """Main function to display content based on selected section"""
    
    if section == "🔧 Step 1: Data Quality Assessment":
        step1.show(project)
    
    elif section == "⚙️ Step 2: Metadata Extraction":
        step2.show(project)
    
    elif section == "🔍 Step 3: Transformation to RPCM Entities":
        step3.show(project)
    
    elif section == "📈 Step 4: Taxonomy Queries":
        step4.show(project)

if __name__ == "__main__":
    main()
