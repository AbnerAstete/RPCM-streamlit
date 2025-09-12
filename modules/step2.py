import streamlit as st

from utils.helpers_step2 import get_project_paths,show_extraction_process

def show(proyecto):
    """Step 2: Metadata Extraction"""
    st.header("⚙️ Step 2: Metadata Extraction")

    st.markdown("""
    In this step, we extract metadata from three sources through the Kaggle API to build a comprehensive 
    understanding of the project. The metadata will be transformed into our standardized JSON format.
    """)
    
    st.image("assets/Step2.svg", caption="Metadata Extraction Step")
    
    st.markdown("---")
    
    # Get project paths
    project_paths = get_project_paths(proyecto)
    # Interactive source selection
    st.subheader("Select Metadata Sources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📋 Project Metadata")
            st.markdown("Get project info via Kaggle API")
            st.markdown("• Author & title")
            st.markdown("• Configuration")
            st.markdown("• Data sources")
            extract_metadata = st.checkbox("Extract Metadata", value=True, key="metadata_check")
        
    with col2:
        with st.container(border=True):
            st.markdown("### 📓 Project Notebook")
            st.markdown("Extract insights from the .ipynb file")
            st.markdown("• Code analysis")
            st.markdown("• Models used")
            st.markdown("• Visualizations")
            extract_notebook = st.checkbox("Extract Notebook", value=True, key="notebook_check")
    
    with col3:
        with st.container(border=True):
            st.markdown("### 📊 Project Outputs")
            st.markdown("Analyze execution results")
            st.markdown("• Log files")
            st.markdown("• Performance")
            st.markdown("• Generated files")
            extract_outputs = st.checkbox("Extract Outputs", value=True, key="outputs_check")
    
    # Show extraction process
    sources_selected = sum([extract_notebook, extract_metadata, extract_outputs])
    
    if sources_selected > 0:
        if st.button("Start Metadata Extraction", type="primary", use_container_width=True):
            show_extraction_process(extract_notebook, extract_metadata, extract_outputs, proyecto, project_paths)
    else:
        st.warning("⚠️ Please select at least one metadata source to continue")


