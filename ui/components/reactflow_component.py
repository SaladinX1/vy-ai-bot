import streamlit as st
import streamlit.components.v1 as components
import json

# Wrapper Streamlit pour react-flow (simplifié)
def reactflow_component(workflow_json):
    component_value = components.declare_component(
        "reactflow_component",
        path="ui/components/reactflow_frontend"  # dossier frontend avec React app
    )
    updated_json = component_value(workflow_json=workflow_json)
    return updated_json
