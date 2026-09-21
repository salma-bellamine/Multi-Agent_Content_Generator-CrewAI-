import streamlit as st
from crew import generate_article


st.set_page_config(
    page_title="Générateur d'Articles IA",
    layout="wide"
)

st.title("Générateur d'Articles IA")

st.write(
    "Générez des articles optimisés pour le SEO "
    "à l'aide d'un système multi-agents basé sur CrewAI."
)


topic = st.text_input(
    "Sujet de l'article",
    placeholder="Exemple : L'intelligence artificielle dans l'éducation"
)

audience = st.text_input(
    "Public cible",
    placeholder="Exemple : Étudiants et enseignants"
)

word_count = st.number_input(
    "Nombre de mots",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

seo_keywords = st.text_input(
    "Mots-clés SEO",
    placeholder="Exemple : intelligence artificielle, éducation, outils IA"
)

description = st.text_area(
    "Description de l'article",
    placeholder=(
        "Décrivez ce que l'article doit expliquer, "
        "le ton souhaité et les points importants à aborder."
    ),
    height=150
)


if st.button("Générer l'article"):

    if not topic:
        st.error("Veuillez saisir le sujet de l'article.")

    elif not audience:
        st.error("Veuillez préciser le public cible.")

    elif not seo_keywords:
        st.error("Veuillez saisir au moins un mot-clé SEO.")

    elif not description:
        st.error("Veuillez saisir une description de l'article.")

    else:

        with st.spinner(
            "Le Planificateur, le Rédacteur et l'Éditeur travaillent..."
        ):

            result = generate_article(
                topic=topic,
                audience=audience,
                word_count=word_count,
                seo_keywords=seo_keywords,
                description=description
            )

        st.success("Article généré avec succès !")

        st.divider()

        st.subheader("Article généré")

        article = str(result)

        st.markdown(article)

        st.download_button(
            label="Télécharger l'article",
            data=article,
            file_name="article_genere.md",
            mime="text/markdown"
        )
