import streamlit as st
import json
import time
import pandas as pd
from datetime import datetime
import uuid

def get_project_paths(proyecto):
    """Get file paths based on project selection"""
    project_mapping = {
        "Student Performance Analysis": "student",
        "Retail Data Analytics": "retail"
    }
    
    project_folder = project_mapping.get(proyecto, "student")
    base_path = f"assets/jsons/metatada_extraction/{project_folder}"
    
    return {
        "entities_kaggle": f"{base_path}/entities-kaggle.json",
        "entities_bulk_atlas": f"{base_path}/entities_bulk_atlas.json"
    }

def load_json_file(file_path):
    """Safely load JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def show_transformation_overview():
    """Show the transformation rules overview"""
    
    st.markdown("#### Transformation Rules")
    st.markdown("Each Kaggle entity type is mapped to corresponding RPCM entities following these rules:")
    
    # Transformation rules in a visual format
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**Process structure Entities**")
            st.markdown("• **Project** → **Project** (Research process definition)")
            st.markdown("• **Owner** → **User** (Process executor/researcher)")
            st.markdown("• **Additional** → **Experiment,Workgroup, Stage, Iteration**")

    with col2:
        with st.container(border=True):
            st.markdown("**Artifacts Entities**")
            st.markdown("• **DataSets** → **UsedData** (Input data resources)")
            st.markdown("• **Log** → **UsedData** (Execution artifacts)")
            st.markdown("• **Notebook** → **Action** (Analysis execution)")
            st.markdown("• **Notebook File** → **UsedData** (File output)")
            st.markdown("• **CodeLine.models** → **UsedData** (Model outputs)")
            st.markdown("• **CodeLine.graphs** → **UsedData** (Visualization outputs)")
    
    # Show entity relationship structure
    st.markdown("#### RPCM Entity Relationships")
    
    relationship_data = {
        "Entity": ["Project", "Experiment", "Stage", "Iteration", "Action", "Action"],
        "Relationship": ["has experiments", "has stages", "has iterations", "executes", "uses", "produces"],
        "Receiving Entity ": ["Experiment", "Stage", "Iteration", "Action", "UsedData (inputs)", "UsedData (outputs)"],
    }
    
    relationship_df = pd.DataFrame(relationship_data)
    st.dataframe(relationship_df, hide_index=True, use_container_width=True)

def show_transformation_process(proyecto):
    """Show the step-by-step transformation process"""
    
    st.subheader("Transformation in Progress...")
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulate transformation steps
    transformation_steps = [
        ("Analyzing Kaggle entities", 0.1),
        ("Generating RPCM Project structure", 0.25),
        ("Creating User and Process entities", 0.4),
        ("Transforming data entities", 0.6),
        ("Building Action workflows", 0.8),
        ("Establishing entity relationships", 0.95),
        ("Finalizing RPCM entities", 1.0)
    ]
    
    for step_name, progress in transformation_steps:
        progress_bar.progress(progress)
        status_text.text(step_name)
        time.sleep(0.8)
    
    status_text.text("Transformation completed successfully!")
    
    if proyecto == "Student Performance Analysis":
        atlas_entities = load_json_file("assets/jsons/atlas_entities/student_entities_bulk_atlas.json")
    elif proyecto == "Retail Data Analytics":
        atlas_entities = load_json_file("assets/jsons/atlas_entities/retail_entities_bulk_atlas.json")

    if atlas_entities:
        show_transformation_results(atlas_entities, proyecto)
    else:
        st.error("Could not load RPCM entities. Please ensure the transformation files are available.")

def analyze_rpcm_entities(atlas_entities):
    """Analyze the RPCM entities and extract key information"""
    
    entities_list = atlas_entities.get("entities", [])
    
    # Count entities by type
    entity_counts = {}
    entity_details = {}
    
    for entity in entities_list:
        entity_type = entity.get("typeName", "Unknown")
        entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1
        
        if entity_type not in entity_details:
            entity_details[entity_type] = []
        entity_details[entity_type].append(entity)
    
    # Count relationships
    total_relationships = 0
    for entity in entities_list:
        if entity.get("relationshipAttributes"):
            for rel_type, rel_list in entity["relationshipAttributes"].items():
                if isinstance(rel_list, list):
                    total_relationships += len(rel_list)
                else:
                    total_relationships += 1
    
    # Get unique GUIDs
    unique_guids = len(set(entity.get("guid") for entity in entities_list if entity.get("guid")))
    
    return {
        "entity_counts": entity_counts,
        "entity_details": entity_details,
        "total_relationships": total_relationships,
        "unique_guids": unique_guids,
        "total_entities": len(entities_list)
    }

def show_transformation_results(atlas_entities, proyecto):
    """Display the transformation results using real RPCM data"""
    
    st.markdown("---")
    st.subheader("Transformation Results")
    
    # Analyze the real entities
    analysis = analyze_rpcm_entities(atlas_entities)
    
    # Summary metrics using real data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Entities", analysis["total_entities"])
    
    with col2:
        st.metric("Entity Types", len(analysis["entity_counts"]))
    
    with col3:
        st.metric("Relationships", analysis["total_relationships"])
    
    with col4:
        st.metric("Unique GUIDs", analysis["unique_guids"])
    
    # Detailed results in tabs
    tab1, tab2, tab3 = st.tabs(["Entity Analysis", "RPCM Structure", "Download Results"])
    
    with tab1:
        show_entity_analysis_results(analysis)
    
    with tab2:
        show_rpcm_structure_results(analysis)
    
    with tab3:
        show_download_results(atlas_entities, proyecto)

def show_entity_analysis_results(analysis):
    """Show detailed entity analysis from real RPCM data"""
    
    st.markdown("### Generated RPCM Entities")
    
    # Entity counts visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Entity Counts by Type**")
        for entity_type, count in analysis["entity_counts"].items():
            st.markdown(f"• **{entity_type}**: {count}")
    
    with col2:
        st.markdown("**Entity Distribution**")
        # Create a simple chart showing entity distribution
        entity_df = pd.DataFrame(list(analysis["entity_counts"].items()), 
                                columns=["Entity Type", "Count"])
        st.bar_chart(entity_df.set_index("Entity Type"))
    
    # Detailed entity information
    st.markdown("### Example Entity")
    
    # Show details for key entity types
    for entity_type, entities in analysis["entity_details"].items():
        if entity_type in ["User", "Project", "Action"]:  # Show details for key entities
            with st.container(border=True):
                st.markdown(f"**{entity_type} Entities ({len(entities)})**")
                
                for entity in entities:
                    attributes = entity.get("attributes", {})
                    name = attributes.get("name", "Unknown")
                    guid = entity.get("guid", "N/A")
                    
                    st.markdown(f"• **{name}** (GUID: `{guid}`)")
                    
                    # Show specific attributes based on entity type
                    if entity_type == "User":
                        role = attributes.get("role", "N/A")
                        st.markdown(f"  - Role: {role}")
                    elif entity_type == "Project":
                        keywords = attributes.get("keywords", [])
                        st.markdown(f"  - Keywords: {', '.join(keywords) if keywords else 'None'}")
                    elif entity_type == "Action":
                        status = attributes.get("status", "N/A")
                        input_data = attributes.get("inputData", "N/A")
                        output_data = attributes.get("outputData", "N/A")
                        st.markdown(f"  - Status: {status}")
                        st.markdown(f"  - Input: {input_data}")
                        st.markdown(f"  - Output: {output_data}")

def show_rpcm_structure_results(analysis):
    """Show the RPCM structure and relationships using real data"""
    
    st.markdown("### RPCM Entity Structure")
    
    # Find key entities for context
    user_entities = analysis["entity_details"].get("User", [])
    project_entities = analysis["entity_details"].get("Project", [])
    
    user_name = "Unknown"
    project_name = "Unknown Project"
    
    if user_entities:
        user_name = user_entities[0].get("attributes", {}).get("name", "Unknown")
    
    if project_entities:
        project_name = project_entities[0].get("attributes", {}).get("name", "Unknown Project")
    
    # Project context using real data
    with st.container(border=True):
        st.markdown("**Project Context**")
        st.markdown(f"• **Project**: {project_name}")
        st.markdown(f"• **Owner**: {user_name}")
        st.markdown(f"• **Total Entities**: {analysis['total_entities']}")
        st.markdown(f"• **Entity Types**: {len(analysis['entity_counts'])}")
    
    # Entity hierarchy with real counts
    with st.container(border=True):
        st.markdown("**Entity Hierarchy (Real Counts)**")
        
        hierarchy_text = f"""
```
Project ({analysis['entity_counts'].get('Project', 0)})
├── Experiment ({analysis['entity_counts'].get('Experiment', 0)})
│   ├── Stage ({analysis['entity_counts'].get('Stage', 0)})
│   │   └── Iteration ({analysis['entity_counts'].get('Iteration', 0)})
│   │       └── Action ({analysis['entity_counts'].get('Action', 0)})
│   │           ├── UsedData ({analysis['entity_counts'].get('UsedData', 0)})
│   │           └── Consensus ({analysis['entity_counts'].get('Consensus', 0)})
│   └── Workgroup ({analysis['entity_counts'].get('Workgroup', 0)})
└── User ({analysis['entity_counts'].get('User', 0)})
```"""
        st.markdown(hierarchy_text)
    
    # UsedData breakdown
    if "UsedData" in analysis["entity_details"]:
        with st.container(border=True):
            st.markdown("**UsedData Breakdown**")
            
            useddata_entities = analysis["entity_details"]["UsedData"]
            data_types = {}
            
            for entity in useddata_entities:
                attributes = entity.get("attributes", {})
                name = attributes.get("name", "")
                
                if "Dataset" in name:
                    data_types["Datasets"] = data_types.get("Datasets", 0) + 1
                elif "Model:" in name:
                    data_types["ML Models"] = data_types.get("ML Models", 0) + 1
                elif "Chart:" in name:
                    data_types["Visualizations"] = data_types.get("Visualizations", 0) + 1
                elif "Notebook:" in name:
                    data_types["Notebooks"] = data_types.get("Notebooks", 0) + 1
                elif "Log:" in name:
                    data_types["Logs"] = data_types.get("Logs", 0) + 1
                else:
                    data_types["Other"] = data_types.get("Other", 0) + 1
            
            for data_type, count in data_types.items():
                st.markdown(f"• **{data_type}**: {count}")

def show_download_results(atlas_entities, proyecto):
    """Show download options for transformation results"""
    
    entities_count = len(atlas_entities.get("entities", []))
    st.markdown(f"**{entities_count} RPCM entities ready for Atlas ingestion**")
    
    # Show a sample of the structure
    preview_data = {
        "entities": atlas_entities.get("entities", [])[:3],  # Show first 3 entities
        "note": f"Showing 3 of {entities_count} entities. Download full file above."
    }
    
    st.code(json.dumps(preview_data, indent=2)[:1000] + "...", language="json")

    st.markdown("### Download Transformation Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download RPCM entities (real data)
        rpcm_json = json.dumps(atlas_entities, indent=2)
        st.download_button(
            label="⬇️ Download RPCM Entities",
            data=rpcm_json,
            file_name=f"{proyecto.lower().replace(' ', '_')}_rpcm_entities.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # Create transformation summary report
        analysis = analyze_rpcm_entities(atlas_entities)
        
        transformation_report = {
            "transformation_report": {
                "project": proyecto,
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_entities": analysis["total_entities"],
                    "entity_types": len(analysis["entity_counts"]),
                    "relationships": analysis["total_relationships"],
                    "unique_guids": analysis["unique_guids"]
                },
                "entity_counts": analysis["entity_counts"]
            }
        }
        
        report_json = json.dumps(transformation_report, indent=2)
        st.download_button(
            label="📊 Download Transformation Report",
            data=report_json,
            file_name=f"{proyecto.lower().replace(' ', '_')}_transformation_report.json",
            mime="application/json",
            use_container_width=True
        )