import os


def CreateMmMusicFromTemplate(trackLines):
    with open(f"{os.getcwd()}/templates/mmMusic.txt", encoding="UTF16") as f:
        templateLines = f.readlines()

    if not os.path.isdir(f"{os.getcwd()}/output"):
        os.mkdir(f"{os.getcwd()}/output")

    with open(f"{os.getcwd()}/output/mmMusic.txt", "w", encoding="UTF16") as f:
        f.writelines(templateLines)
        f.write("\n")
        for line in trackLines:
            f.write(line + "\n")
        f.write("\n")


def CreateMmScoreFromTemplate(scoreLines):
    with open(f"{os.getcwd()}/templates/mmScore.txt", encoding="UTF16") as f:
        templateLines = f.readlines()

    if not os.path.isdir(f"{os.getcwd()}/output"):
        os.mkdir(f"{os.getcwd()}/output")

    with open(f"{os.getcwd()}/output/mmScore.txt", "w", encoding="UTF16") as f:
        f.writelines(templateLines)
        f.write("\n")
        for line in scoreLines:
            f.write(line + "\n")
        f.write("\n")


def CreateSoundBgmFromTemplate(bgmLines):
    with open(f"{os.getcwd()}/templates/SoundBgm.txt", encoding="UTF8") as f:
        templateLines = f.readlines()

    if not os.path.isdir(f"{os.getcwd()}/output"):
        os.mkdir(f"{os.getcwd()}/output")

    with open(f"{os.getcwd()}/output/SoundBGM.txt", "w", encoding="UTF8") as f:
        # Template is not needed anymore as special bgms are handled dynamically
        # f.writelines(templateLines)
        # f.write("\n")

        # Reorder special bgms
        specialBGM = {"tutorial": None, "tutorial_en": None, "omakase": None}

        for enum, line in enumerate(bgmLines):
            splitted = line.split(",")
            if splitted[0] == "TUTORIAL":
                specialBGM["tutorial"] = enum
            elif splitted[0] == "TUTORIAL_EN":
                specialBGM["tutorial_en"] = enum
            elif splitted[0] == "OMAKASE":
                specialBGM["omakase"] = enum

        indexes = []

        # Add special bgms to the top of the file
        for value in specialBGM.values():
            if value is not None:
                # Add that extra space after the comma for these "special bgms"
                splitted = bgmLines[value].split(",")

                f.write(f"{splitted[0]}, {splitted[1]},\n")
                indexes.append(value)

        # Remove special bgms from the list, so they aren't written again
        sorted(indexes, reverse=True)
        print(indexes)
        for indx in indexes:
            bgmLines.pop(indx)

        f.write("\n")

        # Write rest of the lines
        for line in bgmLines:
            f.write(line + "\n")


def CreateMmTextOutEx(lines):
    with open(f"{os.getcwd()}/templates/mmtextout_ex_01.txt", encoding="UTF16") as f:
        templateLinesStart = f.readlines()

    with open(f"{os.getcwd()}/templates/mmtextout_ex_02.txt", encoding="UTF16") as f:
        templateLinesEnd = f.readlines()

    if not os.path.isdir(f"{os.getcwd()}/output"):
        os.mkdir(f"{os.getcwd()}/output")

    with open(f"{os.getcwd()}/output/mmtextout_ex.txt", "w", encoding="UTF16") as f:
        f.writelines(templateLinesStart)
        f.write("\n")
        for line in lines:
            f.write(line + "\n")
        f.writelines(templateLinesEnd)


def CreateMmTextOutJp(lines):
    with open(f"{os.getcwd()}/templates/mmtextout_jp_01.txt", encoding="UTF16") as f:
        templateLinesStart = f.readlines()

    with open(f"{os.getcwd()}/templates/mmtextout_jp_02.txt", encoding="UTF16") as f:
        templateLinesEnd = f.readlines()

    if not os.path.isdir(f"{os.getcwd()}/output"):
        os.mkdir(f"{os.getcwd()}/output")

    with open(f"{os.getcwd()}/output/mmtextout_jp.txt", "w", encoding="UTF16") as f:
        f.writelines(templateLinesStart)
        f.write("\n")
        for line in lines:
            f.write(line + "\n")
        f.writelines(templateLinesEnd)
