from openai import OpenAI

dialog_history=[{"role": "system", "content": "Тебя зовут Раиль. Ты должен будешь отвечать на любой текст.Ты понимаешь татарский язык."},
            {"role": "system","content": "Ты работаешь курьером.На русские слова ты отвечаешь по русский а на татарские по татарский"},
            {"role": "system", "content": "Обычно ты всегда находишься дома"}]

MAX_TOKENS = 4000
def count_tokens(messages):
    # Считаем общее количество токенов в сообщениях
    # Для простоты будем считать, что 1 токен ≈ 1 слово или 4 символа
    return sum(len(msg['content'].split()) for msg in messages)


def response(text):
    global dialog_history
    client = OpenAI()
    dialog_history.append({"role": "user", "content": text})
    while count_tokens(dialog_history) > MAX_TOKENS:
        dialog_history.pop(3)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.7,
        max_completion_tokens=200,
        messages=dialog_history
    )
    assistant_reply = completion.choices[0].message.content
    dialog_history.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply
if __name__ == "__main__":
    print(response("привет, как дела"))
