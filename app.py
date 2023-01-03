import json
import random

import streamlit as st

from datasets import Dataset
from PIL import Image


APP_NAME = "Dreambooth Prompt Annotator"

# Page Configuration
st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_PROMPT = st.text_input("Enter the base prompt for the images")

if BASE_PROMPT:

    FILES = st.file_uploader("Upload the images to annotate", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if FILES:

        state = st.session_state

        if "annotations" not in state:
            state.annotations = {}
            state.files = FILES
            state.current_file = state.files[0]

        def annotate(prompt: str, image: Image):
            """
            Save the current image with the prompt and image to the session state,
            then select a new random image from the list of files.
            """
            state.annotations[state.current_file.name] = {
                "prompt": prompt,
                "image": image,
            }
            if state.files:
                state.current_file = random.choice(state.files)
                state.files.remove(state.current_file)

        st.header("Dataset annotation")

        if state.files:
            selected_file = state.current_file
            st.write(f"Current file: {selected_file}")
            image = Image.open(selected_file)
            st.image(image)

            prompt = st.text_input(
                "Update the base prompt with a more descriptive phrase", key=selected_file, value=BASE_PROMPT
            )
            button = st.button("Next Image", key=f"{selected_file}-button", on_click=annotate, args=(prompt, image))

        else:
            st.info("Everything annotated.")

        st.info(f"Annotated: {len(state.annotations)}, Remaining: {len(state.files)}")

        st.download_button(
            "Download annotations as json",
            # drop the image key from the dict
            json.dumps(
                {k: {k2: v2 for k2, v2 in v.items() if k2 != "image"} for k, v in state.annotations.items()},
                indent=4,
                sort_keys=True,
            ),
        )

        upload = st.button("Upload to HuggingFace Hub")

        if upload:
            holding_list = []
            for annotation in state.annotations.items():
                holding_list.append(annotation[1])
            dataset = Dataset.from_list(holding_list)

            st.text(dataset)
            st.write("Uploading to HuggingFace Hub")
