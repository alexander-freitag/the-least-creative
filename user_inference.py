import requests as r
import time

from os.path import join
from language_detection import detect_language
from translation import translate_german_to_english, translate_bulgarian_to_english
from keyword_extractor import extract_keywords_ollama
from handle_queries import save_query
from handle_articles import format_all_articles



def handle_user_query(query):    
    # Detecting the language of the query
    detected_language = detect_language(query)

    # Translating the query to English if needed
    if detected_language == "de":
        translated_query = translate_german_to_english(query)
    elif detected_language == "bg":
        translated_query = translate_bulgarian_to_english(query)
    elif detected_language == "en":
        translated_query = query
    else:
        raise ValueError("Language not supported or recognized")

    # Extracting keywords from the translated query
    detected_keywords = extract_keywords_ollama(translated_query)
    
    # Ranking the articles based on the keywords
    rank_articles = rank_articles(detected_keywords)
    rank_articles = []

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Save the JSON data to the file
    id = save_query(query, timestamp, detected_keywords, detected_language, rank_articles)
    
    result = {
        'id': id,
        'query': query,
        'timestamp': timestamp,
        'detected_keywords': detected_keywords,
        'detected_language': detected_language,
        'rank_articles': rank_articles
    }
 
    return result


def rank_articles(generated_queries):
    system_prompt = """
        Rank the following articles based on their relevance to the user query.
        Use only the articles that are most relevant to the user query.
        If there are a lot of relevant articles, you can use the 10 articles.
        Return only the IDs of the articles in descending order of relevance.
        Do not include any additional information."""

    article_string = format_all_articles(sample_list)
    user_prompt = "User Query: " + generated_queries + "\n\n" + "Articles: " + "\n".join(format_all_articles(article_string))

    ranking_data = {
        "model": "llama3",
        "raw": False,
        "prompt": f"{user_prompt}",
        "system": f"{system_prompt}",
        "stream": False,
    }

    ranking_response = r.post("http://localhost:11434/api/generate", json=ranking_data)
    ranking_response = ranking_response.json()
    ranking_response = ranking_response["response"]

    print(ranking_response)

    return ranking_response



sample_list = [
    {'id': 1, 'keywords': ['quantum mechanics', 'wave-particle duality', 'uncertainty principle']},
    {'id': 2, 'keywords': ['general relativity', 'black holes', 'cosmology']},
    {'id': 3, 'keywords': ['thermodynamics', 'entropy', 'heat transfer']},
    {'id': 4, 'keywords': ['electromagnetism', 'Maxwell\'s equations', 'electromagnetic waves']},
    {'id': 5, 'keywords': ['nuclear physics', 'radioactivity', 'nuclear reactions']},
    {'id': 6, 'keywords': ['particle physics', 'elementary particles', 'particle accelerators']},
    {'id': 7, 'keywords': ['optics', 'light', 'lenses']},
    {'id': 8, 'keywords': ['fluid mechanics', 'Bernoulli\'s principle', 'viscosity']},
    {'id': 9, 'keywords': ['astrophysics', 'stellar evolution', 'galactic dynamics']},
    {'id': 10, 'keywords': ['solid state physics', 'crystal structure', 'semiconductor devices']},
    {'id': 11, 'keywords': ['acoustics', 'sound waves', 'musical instruments']},
    {'id': 12, 'keywords': ['plasma physics', 'fusion energy', 'magnetic confinement']},
    {'id': 13, 'keywords': ['condensed matter physics', 'superconductivity', 'quantum materials']},
    {'id': 14, 'keywords': ['atomic physics', 'quantum states', 'spectroscopy']},
    {'id': 15, 'keywords': ['biophysics', 'biological systems', 'biomedical imaging']},
    {'id': 16, 'keywords': ['statistical mechanics', 'thermodynamic ensembles', 'phase transitions']},
    {'id': 17, 'keywords': ['cosmology', 'dark matter', 'dark energy']},
    {'id': 18, 'keywords': ['quantum field theory', 'particle interactions', 'quantum electrodynamics']},
    {'id': 19, 'keywords': ['gravitational waves', 'LIGO', 'black hole mergers']},
    {'id': 20, 'keywords': ['atomic and molecular physics', 'quantum chemistry', 'photoionization']},
    {'id': 21, 'keywords': ['nuclear astrophysics', 'stellar nucleosynthesis', 'supernovae']},
    {'id': 22, 'keywords': ['optoelectronics', 'photovoltaics', 'light-emitting diodes']},
    {'id': 23, 'keywords': ['high energy physics', 'colliders', 'Higgs boson']},
    {'id': 24, 'keywords': ['quantum computing', 'qubits', 'quantum algorithms']},
    {'id': 25, 'keywords': ['plasma astrophysics', 'solar wind', 'magnetic reconnection']},
    {'id': 26, 'keywords': ['condensed matter theory', 'topological phases', 'quantum spin liquids']},
    {'id': 27, 'keywords': ['atomic and molecular spectroscopy', 'laser cooling', 'ultrafast dynamics']},
    {'id': 28, 'keywords': ['biomedical physics', 'medical imaging', 'radiation therapy']},
    {'id': 29, 'keywords': ['quantum optics', 'entangled photons', 'quantum teleportation']},
    {'id': 30, 'keywords': ['astroparticle physics', 'dark matter detection', 'neutrino oscillations']},
    {'id': 31, 'keywords': ['nanophysics', 'nanomaterials', 'nanoelectronics']},
    {'id': 32, 'keywords': ['quantum gravity', 'string theory', 'black hole information paradox']},
    {'id': 33, 'keywords': ['plasma diagnostics', 'magnetic confinement fusion', 'plasma instabilities']},
    {'id': 34, 'keywords': ['quantum simulation', 'ultracold atoms', 'quantum phase transitions']},
    {'id': 35, 'keywords': ['medical physics', 'radiation therapy', 'dosimetry']},
    {'id': 36, 'keywords': ['quantum information', 'quantum entanglement', 'quantum error correction']},
    {'id': 37, 'keywords': ['astrophysical fluid dynamics', 'magnetohydrodynamics', 'accretion disks']},
    {'id': 38, 'keywords': ['quantum materials', 'topological insulators', 'strongly correlated systems']},
    {'id': 39, 'keywords': ['atomic and molecular collisions', 'electron scattering', 'photoionization']},
    {'id': 40, 'keywords': ['plasma physics applications', 'plasma processing', 'plasma propulsion']},
    {'id': 41, 'keywords': ['quantum metrology', 'atomic clocks', 'quantum sensors']},
    {'id': 42, 'keywords': ['astrophysical simulations', 'cosmological simulations', 'galaxy formation']},
    {'id': 43, 'keywords': ['quantum optics', 'cavity quantum electrodynamics', 'quantum memories']},
    {'id': 44, 'keywords': ['quantum chemistry', 'molecular dynamics', 'chemical reactions']},
    {'id': 45, 'keywords': ['plasma physics theory', 'kinetic theory', 'wave-particle interactions']},
    {'id': 46, 'keywords': ['quantum materials synthesis', 'thin films', 'nanoparticles']},
    {'id': 47, 'keywords': ['astrophysical magnetohydrodynamics', 'magnetic fields', 'dynamo theory']},
    {'id': 48, 'keywords': ['quantum computing hardware', 'superconducting qubits', 'topological qubits']},
    {'id': 49, 'keywords': ['plasma physics experiments', 'magnetic confinement', 'laser-plasma interactions']},
    {'id': 50, 'keywords': ['quantum gravity', 'loop quantum gravity', 'quantum black holes']}
]

rank_articles("black holes, universe, galaxies, stars, astronomy")