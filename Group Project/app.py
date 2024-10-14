import gradio as gr

# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Tianlin668/MentalBART")
model = AutoModelForSeq2SeqLM.from_pretrained("Tianlin668/MentalBART")

# Define the inference function
def inference(prompt):

    # Encode the input prompt
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Generate a response
    # You can adjust max_length and num_beams according to your needs
    output = model.generate(input_ids, max_length=150, num_beams=5, early_stopping=True)

    # Decode the generated output
    result = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Return the generated response from the model
    return result

with gr.Blocks() as demo:
    gr.Markdown("<center><h1> This is your virtual assistant - MentalBART model </h1></center>")
    gr.Markdown("<center><h2> This assistant will try to diagnose for depression and provide reasoning for it. </h2></center>")

    # Input boxes for the prompt and Hugging Face token
    prompt = gr.Textbox(label="Prompt", lines=3, max_lines=5)
    
    # Button for generating response
    generate_btn = gr.Button("Generate Response")
    output = gr.Markdown("Response will appear here.")
    
    # Trigger the inference function on button click
    generate_btn.click(fn=inference, inputs=[prompt], outputs=[output])
    

if __name__ == "__main__":
    demo.launch()
