import gradio as gr
from assistant import AIAssistant


async def setup():
    agent = AIAssistant()
    await agent.setup()
    return agent


async def process_message(agent, message, success_criteria, history):
    results = await agent.run_superstep(message, success_criteria, history)
    return results, agent


async def reset():
    new_agent = AIAssistant()
    await new_agent.setup()
    return "", "", None, new_agent


def free_resources(agent):
    print("Cleaning up")
    try:
        if agent:
            agent.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


with gr.Blocks(title="AI Assistant Agent", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## AI Assistant Agent")
    agent = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Assistant", height=300, type="messages")
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the assistant")
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="What are your success criteria?"
            )
    with gr.Row():
        reset_button = gr.Button("Reset", variant="stop")
        go_button = gr.Button("Go!", variant="primary")

    ui.load(setup, [], [agent])
    message.submit(
        process_message, [agent, message, success_criteria, chatbot], [chatbot, agent]
    )
    success_criteria.submit(
        process_message, [agent, message, success_criteria, chatbot], [chatbot, agent]
    )
    go_button.click(
        process_message, [agent, message, success_criteria, chatbot], [chatbot, agent]
    )
    reset_button.click(reset, [], [message, success_criteria, chatbot, agent])


if __name__ == "__main__":
    ui.launch(inbrowser=True)
