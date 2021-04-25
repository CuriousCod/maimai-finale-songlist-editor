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
        f.writelines(templateLines)
        f.write("\n")
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
