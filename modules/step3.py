import streamlit as st

from utils.helpers_step3 import show_transformation_overview,show_transformation_process

def show(proyecto):
    """Step 3: Transformation to RPCM Entities"""
    st.header("🔍 Step 3: Transformation to RPCM Entities")

    st.markdown("""
    In this step we apply a series of transformation rules to convert the Kaggle metamodel entities into RPCM entities, 
    generating a set of entities ready to be ingested into Apache Atlas. These new entities are connected through unique 
    identifiers, allowing the system to track what was done, who did it, with which data, in which order, and what results were obtained.
    """)
    
    st.image("assets/step3.svg", caption="Transformation to RPCM Entities Step")
    
    st.markdown("---")
    
    # Transformation Overview
    show_transformation_overview()
    
    st.markdown("---")
    
    # Interactive transformation process
    if st.button("Start RPCM Transformation", type="primary", use_container_width=True):
        show_transformation_process(proyecto)

