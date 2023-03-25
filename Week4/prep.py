def prep(s): # inputs 210 x 160 x 3 and returns 95 x 80
    h = 210
    w = 160
    s = [[0.2989*s[2*i][2*j][0] + 0.5870*s[2*i][2*j][1] + 0.1140*s[2*i][2*j][2] for j in range(int(w / 2))] for i in range(int(h / 2))]
    s = s[10:]
    return s
