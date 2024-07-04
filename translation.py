import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# Load the fine-tuned model and tokenizer
model_de = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-en")
tokenizer_de = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-en")
model_bg = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-bg-en")
tokenizer_bg = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-bg-en")

device = 0 if torch.cuda.is_available() else -1
# Create a translation pipeline
translation_pipeline_de_en = pipeline("translation_de_to_en", model=model_de, tokenizer=tokenizer_de, device=device)
translation_pipeline_bg_en = pipeline("translation_bg_to_en", model=model_bg, tokenizer=tokenizer_bg, device=device)


def split_text_by_periods(text, num_periods=5):
    # Sätze anhand von Punkt aufteilen
    sentences = text.split('. ')
    chunks = []

    for i in range(0, len(sentences), num_periods):
        chunk = '. '.join(sentences[i:i + num_periods])
        if chunk[-1] != '.':
            chunk += '.'
        chunks.append(chunk)

    return chunks
# Function to translate German text to English
def translate_german_to_english(german_text):
    translated_text = []
    for sentence in split_text_by_periods(german_text):
        translated_text.append(translation_pipeline_de_en(sentence))
    return "".join(e[0]['translation_text'] for e in translated_text)


# Function to translate Bulgarian text to English
def translate_bulgarian_to_english(bulgarian_text):
    translated_text = []
    for sentence in split_text_by_periods(bulgarian_text):
        translated_text.append(translation_pipeline_de_en(sentence))
    return "".join(e[0]['translation_text'] for e in translated_text)


print(translate_german_to_english("Der Frühling ist die schönste Jahreszeit. Wenn die Tage länger werden und die Sonne wärmer scheint, erwacht die Natur zu neuem Leben. Die Bäume bekommen frische grüne Blätter, und überall blühen Blumen in den schönsten Farben. Die Vögel kehren aus ihren Winterquartieren zurück und beginnen mit ihrem fröhlichen Gesang. Überall summen Bienen und Schmetterlinge flattern von Blüte zu Blüte. In dieser Zeit genießen viele Menschen die ersten warmen Tage im Freien. Man unternimmt Spaziergänge im Park oder in der Natur, fährt mit dem Fahrrad oder trifft sich mit Freunden zum Grillen im Garten. Die Kinder spielen wieder draußen, rennen über Wiesen und bauen Sandburgen im Sandkasten. Auch die ersten Ausflüge zum nahegelegenen See oder ins Schwimmbad stehen auf dem Programm. Nicht nur die Menschen freuen sich über das Erwachen der Natur. Auch die Tiere sind aktiver und man kann häufig Hasen, Rehe und andere Wildtiere beobachten. Besonders in den frühen Morgenstunden oder in der Dämmerung sieht man sie auf den Feldern und im Wald. Die Tierkinder kommen zur Welt, und es ist ein besonderes Erlebnis, die jungen Rehe oder Fohlen beim Spielen zu beobachten. Der Frühling ist aber auch eine Zeit des Neubeginns und der Erneuerung. Viele Menschen nutzen diese Jahreszeit,"))