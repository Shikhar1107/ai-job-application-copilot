from langgraph.graph import END, START, StateGraph
from app.ai.nodes.matching_nodes import match_skills_node
from app.ai.nodes.scoring_nodes import score_fit_node
from app.ai.nodes.skill_extraction_nodes import extract_skills_node
from app.ai.state import JobAnalysisState

def build_job_analysis_graph():
    graph_builder = StateGraph(JobAnalysisState)
    graph_builder.add_node("extract_skills", extract_skills_node)
    graph_builder.add_node("match_skills", match_skills_node)
    graph_builder.add_node("score_fit", score_fit_node)
    
    graph_builder.add_edge(START, "extract_skills")
    graph_builder.add_edge("extract_skills","match_skills")
    graph_builder.add_edge("match_skills","score_fit")
    graph_builder.add_edge("score_fit",END)

    return graph_builder.compile()

job_analysis_graph = build_job_analysis_graph()

