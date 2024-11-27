import gradio as gr
import atproto as atp
from text_summarization_docker import text_inference


client = atp.Client()


def get_auth(username: str, password: str) -> bool:
    global client
    try:
        client.login(username, password)
        return True
    except Exception as e:
        return False

def get_feed():
    strtort = ""
    strsum = ""
    # Get "Home" page. Use pagination (cursor + limit) to fetch all posts
    timeline = client.get_timeline(algorithm='reverse-chronological')
    for feed_view in timeline.feed:
        action = 'New Post🆕'
        if feed_view.reason:
            action_by = feed_view.reason.by.handle
            action = f'Reposted by @{action_by}🔁'

        post = feed_view.post.record
        author = feed_view.post.author

        strtort += f'### {action}\n\n<img alt="Avatar for {author.display_name}" src="{author.avatar}" width=50> **{author.display_name}**:\n\n{post.text}\n\n-------------------\n\n'
        strsum += f'Author: {author.display_name} - Post content: {post.text}'
    chat_hist = [{"role": "system", "content": "You are a helpful and efficient feed summarization assistant. You should provide a coincise and well-style, polished overview of what the post authors are telling"}, {"role": "user", "content": strsum}]
    res = text_inference(chat_hist)
    smry = f"\n\n<details>\n\t<summary><b>Feed Summary</b></summary>\n\n{res}\n\n</details>\n\n"
    strtort = f"<div align='center'>\n\t<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Bluesky_Logo.svg/1920px-Bluesky_Logo.svg.png' alt='BlueSky Logo' width=150>\n</div>\n<br>\n\n## Home Feed (Following)🏠\n\n----------------------\n\n{smry}\n\n{strtort}"
    return strtort

iface = gr.Interface(fn=get_feed, inputs=None, outputs=gr.Markdown(), title="BlueSky User Feed", theme='shivi/calm_seafoam')
iface.launch(auth=get_auth, auth_message="Insert here your BlueSky username/handle and your password", server_name="0.0.0.0", server_port=7860)
