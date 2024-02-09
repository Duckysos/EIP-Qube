import pvporcupine


porcupine = pvporcupine.create(
  access_key='YcqT9Njmr3eqJQkf/nZNeDp0k5vX4OOHfvyrdsPf9IChaK36XJxu8w==',
  keyword_paths=["C:\\Users\\user\\OneDrive\\Desktop\\Qube\\Hello-Cube_en_windows_v3_0_0.ppn"]
)


while True:

    try:
        with sr.Microphone() as mic:

            sr.adjust_for_ambient_noise(mic, duration = 0.2)
            audio = sr.listen(mic)

            keyword_paths = porcupine.process(audio)

            if keyword_paths == 0:
                print("Hello Cube detected!")

    except sr.UnknownValueError():

        r = sr.Recognizer()
        continue

    

