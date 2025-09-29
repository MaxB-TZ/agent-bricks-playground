import streamlit as st
import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Databricks Agent Bricks Tester",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1rem;
        text-align: center;
    }

    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
        text-align: center;
    }

    .agent-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 0.875rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.2s;
        position: relative;
    }

    .agent-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
        transform: translateY(-1px);
    }

    .agent-card.selected {
        border-color: #3b82f6;
        background: #f8fafc;
        box-shadow: 0 0 0 1px #3b82f6;
    }

    .agent-name {
        font-size: 0.875rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .agent-model {
        font-size: 0.75rem;
        color: #4b5563;
        font-family: monospace;
        background: #f1f5f9;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        margin-bottom: 0.5rem;
        display: inline-block;
    }

    .agent-endpoint {
        font-size: 0.7rem;
        color: #6b7280;
        font-family: monospace;
        background: #f8fafc;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        margin-bottom: 0.5rem;
        word-break: break-all;
        line-height: 1.3;
    }

    .agent-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }

    .agent-delete-btn {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
        border-radius: 0.375rem;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    .agent-delete-btn:hover {
        background: #dc2626;
        color: white;
    }

    .section-header {
        font-size: 0.875rem;
        font-weight: 600;
        color: #374151;
        margin: 1.5rem 0 0.75rem 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .section-header:first-child {
        margin-top: 0;
    }

    .empty-state {
        text-align: center;
        padding: 1.5rem 1rem;
        color: #6b7280;
        font-size: 0.875rem;
    }

    .empty-state-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        opacity: 0.5;
    }

    .test-container {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    .response-container {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
        font-family: monospace;
        font-size: 0.875rem;
        white-space: pre-wrap;
        color: #1f2937;
        line-height: 1.5;
    }

    .success-message {
        color: #059669;
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }

    .error-message {
        color: #dc2626;
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 0.5rem;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }

    .auth-status {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.375rem;
        padding: 0.5rem 0.75rem;
        margin: 0.5rem 0;
        text-align: center;
        font-size: 0.75rem;
    }

    .auth-status.authenticated {
        background: #f0fdf4;
        border-color: #bbf7d0;
        color: #166534;
    }

    .auth-status.not-authenticated {
        background: #fef2f2;
        border-color: #fecaca;
        color: #dc2626;
    }

    .auth-section {
        margin-top: auto;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }

    .auth-button {
        font-size: 0.75rem;
        padding: 0.5rem 0.75rem;
    }

    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .modal-content {
        background: white;
        border-radius: 0.75rem;
        padding: 2rem;
        max-width: 500px;
        width: 90%;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }
</style>
""", unsafe_allow_html=True)

class AgentManager:
    def __init__(self):
        self.config_file = "agents_config.yaml"
        self.load_agents()

    def load_agents(self):
        """Load agents from config file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.agents = yaml.safe_load(f) or {}
        else:
            self.agents = {}

    def save_agents(self):
        """Save agents to config file"""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.agents, f, default_flow_style=False)

    def add_agent(self, name, endpoint, model):
        """Add a new agent"""
        self.agents[name] = {
            'endpoint': endpoint,
            'model': model,
            'created_at': datetime.now().isoformat()
        }
        self.save_agents()

    def delete_agent(self, name):
        """Delete an agent"""
        if name in self.agents:
            del self.agents[name]
            self.save_agents()

    def get_agent(self, name):
        """Get agent details"""
        return self.agents.get(name)

def test_agent(agent_name, endpoint, model, message, token):
    """Test an agent with a given message"""
    try:
        client = OpenAI(
            api_key=token,
            base_url=endpoint
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        # Extract usage information properly
        usage_info = None
        if response.usage:
            usage_info = {
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens
            }

        return {
            'success': True,
            'content': response.choices[0].message.content,
            'usage': usage_info
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def show_auth_modal():
    """Show authentication modal"""
    with st.container():
        st.markdown("""
        <div class="modal" id="authModal">
            <div class="modal-content">
                <h3>🔐 Authentication</h3>
                <p>Enter your Databricks token to test agents</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Initialize agent manager
    agent_manager = AgentManager()

    # Initialize session state for auth modal
    if 'show_auth_modal' not in st.session_state:
        st.session_state.show_auth_modal = False

    # Main header
    st.markdown('<h1 class="main-header">🤖 Databricks Agent Bricks Tester</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Test and interact with your Databricks Agent Bricks agents</p>', unsafe_allow_html=True)

    # Sidebar for agent management
    with st.sidebar:
        # Header
        st.markdown("## 🤖 Agent Bricks Tester")

        # Add new agent section
        st.markdown('<div class="section-header">➕ Add New Agent</div>', unsafe_allow_html=True)
        with st.expander("Create Agent", expanded=False):
            with st.form("add_agent_form"):
                agent_name = st.text_input("Agent Name", placeholder="My Agent")
                agent_endpoint = st.text_input("Endpoint URL", placeholder="https://dbc-xxxxx.cloud.databricks.com/serving-endpoints")
                agent_model = st.text_input("Model Name", placeholder="t2t-xxxxx-endpoint")

                if st.form_submit_button("Add Agent", use_container_width=True):
                    if agent_name and agent_endpoint and agent_model:
                        agent_manager.add_agent(agent_name, agent_endpoint, agent_model)
                        st.success(f"Agent '{agent_name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill in all fields")

        # Agent list section
        st.markdown('<div class="section-header">🤖 Your Agents</div>', unsafe_allow_html=True)

        if not agent_manager.agents:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🤖</div>
                <div>No agents configured</div>
                <div style="font-size: 0.75rem; margin-top: 0.5rem;">Add one using the form above</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display agents as cards
            for name, details in agent_manager.agents.items():
                # Check if this agent is selected
                is_selected = st.session_state.get('selected_agent') == name
                card_class = "agent-card selected" if is_selected else "agent-card"

                st.markdown(f"""
                <div class="{card_class}">
                    <div class="agent-name">
                        <span>{name}</span>
                        <span style="font-size: 0.75rem; color: #6b7280;">🤖</span>
                    </div>
                    <div class="agent-model">{details['model']}</div>
                    <div class="agent-endpoint">{details['endpoint']}</div>
                </div>
                """, unsafe_allow_html=True)

                # Agent actions
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Select", key=f"select_{name}", use_container_width=True):
                        st.session_state.selected_agent = name
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"delete_{name}", use_container_width=True, help="Delete agent"):
                        agent_manager.delete_agent(name)
                        if st.session_state.get('selected_agent') == name:
                            st.session_state.selected_agent = None
                        st.rerun()

        # Authentication section - moved to bottom with subtle styling
        st.markdown('<div class="auth-section">', unsafe_allow_html=True)

        # Check if token exists
        env_token = os.getenv('DATABRICKS_TOKEN')
        has_token = bool(env_token)

        if has_token:
            st.markdown('<div class="auth-status authenticated">🔑 Authenticated</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="auth-status not-authenticated">🔓 Not Authenticated</div>', unsafe_allow_html=True)

        # Auth modal trigger button - more subtle
        if st.button("Manage Auth", use_container_width=True, key="auth_button"):
            st.session_state.show_auth_modal = True
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Show auth modal if triggered
        if st.session_state.show_auth_modal:
            with st.expander("🔐 Authentication Settings", expanded=True):
                st.markdown("**Current Status:**")
                if has_token:
                    st.success("✅ Token loaded from .env file")
                    st.caption("Your token is automatically loaded from the .env file")
                else:
                    st.warning("⚠️ No token found in .env file")
                    st.caption("Add DATABRICKS_TOKEN to your .env file or enter manually below")

                st.markdown("**Manual Token Entry:**")
                manual_token = st.text_input(
                    "Databricks Token",
                    type="password",
                    help="Enter your Databricks personal access token",
                    placeholder="Enter your Databricks token...",
                    key="manual_token"
                )

                if manual_token:
                    st.session_state.manual_token = manual_token
                    st.success("✅ Token set for this session")

                st.markdown("**Environment Setup:**")
                st.code("""
# Create .env file with:
DATABRICKS_TOKEN=your_token_here
                """, language="bash")

                if st.button("Close", use_container_width=True):
                    st.session_state.show_auth_modal = False
                    st.rerun()

    # Main content area
    if not agent_manager.agents:
        st.info("👆 Add your first agent using the sidebar to get started!")
        return

    # Get selected agent from sidebar
    selected_agent = st.session_state.get('selected_agent')

    if not selected_agent:
        st.info("👈 Select an agent from the sidebar to start testing!")
        st.markdown("""
        ### How to get started:
        1. **Add an agent** using the "Create Agent" form in the sidebar
        2. **Select the agent** by clicking the "Select" button on any agent card
        3. **Authenticate** using the "Manage Authentication" button
        4. **Start testing** your agent!
        """)
        return

    if selected_agent:
        agent_details = agent_manager.get_agent(selected_agent)

        # Display selected agent info
        st.markdown(f"### 🤖 Testing: {selected_agent}")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**Endpoint:** `{agent_details['endpoint']}`")
        with col2:
            st.markdown(f"**Model:** `{agent_details['model']}`")

        # Get token from environment or session state
        env_token = os.getenv('DATABRICKS_TOKEN')
        manual_token = st.session_state.get('manual_token', '')
        token = env_token or manual_token

        if not token:
            st.warning("⚠️ Please authenticate using the sidebar to test the agent")
            st.info("Click '🔐 Manage Authentication' in the sidebar to set up your token")
            return

        # Test interface
        st.subheader("Test Interface")

        # Message input
        message = st.text_area(
            "Message to Agent",
            placeholder="What would you like to ask the agent?",
            height=100,
            help="Enter your message or question for the agent"
        )

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🚀 Send Message", use_container_width=True, type="primary"):
                if message.strip():
                    with st.spinner("Testing agent..."):
                        result = test_agent(
                            selected_agent,
                            agent_details['endpoint'],
                            agent_details['model'],
                            message,
                            token
                        )

                    if result['success']:
                        st.success("✅ Agent responded successfully!")
                        st.markdown("**Response:**")
                        st.code(result["content"], language=None)

                        if result.get('usage'):
                            with st.expander("📊 Usage Information", expanded=False):
                                usage = result['usage']
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.metric("Prompt Tokens", usage.get('prompt_tokens', 'N/A'))
                                with col2:
                                    st.metric("Completion Tokens", usage.get('completion_tokens', 'N/A'))
                                with col3:
                                    st.metric("Total Tokens", usage.get('total_tokens', 'N/A'))

                                # Show raw JSON for debugging
                                with st.expander("Raw Usage Data", expanded=False):
                                    st.json(usage)
                        else:
                            st.info("ℹ️ No usage information available for this response")
                    else:
                        st.error(f"❌ Error: {result['error']}")
                else:
                    st.warning("Please enter a message to send")

        with col2:
            if st.button("🧹 Clear", use_container_width=True):
                st.rerun()

                if result['success']:
                    st.success("✅ Agent responded successfully!")
                    st.markdown("**Response:**")
                    st.code(result["content"], language=None)
                else:
                    st.error(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    main()
