import json
import matplotlib.pyplot as plt

finger_data = {
    0: "WRIST",
    1: "THUMB_CMC",
    2: "THUMB_MCP",
    3: "THUMB_IP",
    4: "THUMB_TIP",
    5: "INDEX_FINGER_MCP",
    6: "INDEX_FINGER_PIP",
    7: "INDEX_FINGER_DIP",
    8: "INDEX_FINGER_TIP",
    9: "MIDDLE_FINGER_MCP",
    10: "MIDDLE_FINGER_PIP",
    11: "MIDDLE_FINGER_DIP",
    12: "MIDDLE_FINGER_TIP",
    13: "RING_FINGER_MCP",
    14: "RING_FINGER_PIP",
    15: "RING_FINGER_DIP",
    16: "RING_FINGER_TIP",
    17: "PINKY_MCP",
    18: "PINKY_PIP",
    19: "PINKY_DIP",
    20: "PINKY_TIP"
}



with open("data.json") as f:
    f = f.read()
    f = json.loads(f)
    plt.rcParams.update({'font.size': 10})
    for coor in ["x", "y", "z"]:
        dataList = {}
        for i in range(20):
            dataList[finger_data[i]] = [obj[str(i)][coor] for obj in f]

        plt.figure(figsize=[10, 8])
        plt.title(coor)
        i = 1
        for name, data in dataList.items():
            plt.subplot(5, 4, i)
            i += 1
            plt.plot(range(len(data)), data)
            plt.title(name, fontsize=7)
            plt.xticks([])
            plt.yticks([])
        plt.xticks([])
        plt.yticks([])
    plt.show()
