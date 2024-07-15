import random, math
import tkinter as tk

def assorment_calculation(geneB_input:list, geneP_input:list, l_input:list, M:list):

    geneB = geneB_input
    geneP = geneP_input
    l =  l_input

    #step 2
    I = [[[]] for i in range(len(M))]
    k = [0 for i in range(len(M))]
    tc = geneB[0]

    #step 3
    for i in range(len(l)):
        if k[geneB[i]-1] == 0:
            k[geneB[i]-1] = 1
        if geneB[i] != tc:
            tc = geneB[i]
        assign = False
        for j in I[tc-1]:
            if geneB[i] == tc and sum(j)+l[i] <= M[tc-1]:
                j.append(l[i])

                assign = True
                
                break
        if assign == False:
            I[tc-1].append([l[i]])
            k[geneB[i]-1] += 1
        else:
            continue

        
            # print('hhh')
        # 3.5, 2.7, 2.2, 2.2, 1.9, 1.7, 1.5
        # print(I)
        # print([sum(I[i]) for i in range(len(M))])
    I_disatuin=[]
    for i in range(len(I)):
        b=[]
        for j in range(len(I[i])):
            for o in range(len(I[i][j])):
                a = I[i][j][o]
                b.append(a)
        I_disatuin.append(b)

    #     print('I disatuin:', I_disatuin)
    # print('kTotal:',k)
    # print ('I lama: ', I)
    I_tidakDisatuin = I[:]
    I = I_disatuin[:]
    # print('I:', I)

    return I, k, geneB, geneP, l, I_tidakDisatuin

def objective(k:list, M:list):

    J = 0

    for i in range(len(M)):
        J += k[i]*(M[i])
    return J
def yield_rate(l:list, J:int):
    return (round(sum(l),1))/J

def fitness(k:list, M:list, l:list): 

    J = objective(k, M)
    if yield_rate(l, J) < 0.55:

        return (10/55)*yield_rate(l, J)
    
    else:
        
        return 2*yield_rate(l, J) - 1
    
def snipping_rate_t(I:list, k:list, M:list, t:int):

    if k[t] == 0:
        return (1 - (round(sum(I[t]),1)/(M[t])))
    else:
        return (1 - (round(sum(I[t]),1)/(k[t]*M[t])))
def reviseGeneP(I:list, k:list, M:list, l:list, geneB:list, geneP:list):
    
    for i in range(len(l)):
        geneP[i] = snipping_rate_t(I,k,M, geneB[i]-1)
    return geneP

def control_crossover_parameter(snip_rate):

    r = snip_rate
    if r < 0.05:

        return 2400*r**3
    
    else:

        return min(0.8 * (r-0.05)**(1/4) + 0.3,1)


def selection(populasi:list, kumpulan_fitness:list):

    kromosom_terpilih = [] # kumpulan kromosom yang terpilih

    #Elitist Selection
    elitist = populasi[kumpulan_fitness.index(max(kumpulan_fitness))]
    kromosom_terpilih.append(elitist) # Dipilih 1 kromosom dari populasi saat ini dengan fitness terbesar 

    #Roulette Wheel
    p = []
    c = []
    for i in range(len(kumpulan_fitness)): 
        p.append(kumpulan_fitness[i]/sum(kumpulan_fitness))
        if i > 0:
            c.append(c[i-1]+p[i])
        else:
            c.append(p[i])

    while len(kromosom_terpilih) != 4: # Dipilih 3 kromosom dari populasi saat ini dengan roulette wheel
        r = random.random()
        for j in range(len(c)-1):
            if r > c[j] and  r <= c[j+1]:
                kromosom_terpilih.append(populasi[c.index(c[j+1])]) 

    return kromosom_terpilih # Terpilih 4 kromosom dari populasi saat ini

def pilih_parent(kromosom_terpilih:list, sel_probability):

    parent_terpilih = []

    i = 0
    while len(parent_terpilih) != 2:
        r = random.random()
        if r < sel_probability:
            parent_terpilih.append(kromosom_terpilih[i])
            i = ((i + 1) % (len(kromosom_terpilih)))
        else:
            i = ((i + 1) % (len(kromosom_terpilih)))
        
    return parent_terpilih
def crossover(kromosom_terpilih:list, kumpulan_l:list, kumpulan_snip_p:list, populasi:list, sel_probability):
    
    parent_terpilih = pilih_parent(kromosom_terpilih,sel_probability) # Memilih parent

    geneB_Par_1 = parent_terpilih[0][0] # parent_terpilih[0][0] merupakan geneB dari parent ke-1
    geneP_Par_1 = parent_terpilih[0][1] # parent_terpilih[0][1] merupakan geneP dari parent ke-1
    geneB_Par_2 = parent_terpilih[1][0] # parent_terpilih[1][0] merupakan geneB dari parent ke-2
    geneP_Par_2 = parent_terpilih[1][1] # parent_terpilih[1][1] merupakan geneP dari parent ke-2

     
    # Diinisialisasikan terlebih dahulu geneB & geneP child

    geneB_Ch_1 = geneB_Par_1[:]
    geneP_Ch_1 = geneP_Par_1[:]
    geneB_Ch_2 = geneB_Par_2[:]
    geneP_Ch_2 = geneP_Par_2[:]
    
    snip_Par_1 = kumpulan_snip_p[populasi.index(parent_terpilih[0])] # kumpulan snipping rate mother material dari parent 1
    snip_Par_2 = kumpulan_snip_p[populasi.index(parent_terpilih[1])] # kumpulan snipping rate mother material dari parent 2

    for i in range(len(geneB_Par_1)):

        #Child 1
        r = snip_Par_1[geneB_Par_1[i]-1]
        p = control_crossover_parameter(r)
        # print('par 2',geneB_Par_2)
        if p > random.random():
            geneB_Ch_1[i] = geneB_Par_2[i]
            geneP_Ch_1[i] = geneP_Par_2[i]

        else:
            continue
        
        #Child 2
        r = snip_Par_2[geneB_Par_2[i]-1]
        p = control_crossover_parameter(r)

        if p > random.random():
            geneB_Ch_2[i] = geneB_Par_1[i]
            geneP_Ch_2[i] = geneP_Par_1[i]

        else:
            continue
    
    child_hasil = [[] for i in range(2)]
    # menginput geneB dan geneP ke dalam kromosom child
    child_hasil[0].append(geneB_Ch_1)
    child_hasil[0].append(geneP_Ch_1)
    child_hasil[1].append(geneB_Ch_2)
    child_hasil[1].append(geneP_Ch_2)

    return child_hasil

def mutation(kromosom_terpilih:list, M:list, kumpulan_l:list, geneB_mut_prob, geneB_mut_locus_num, geneP_mut_prob, geneP_mut_locus_num):
    
    # Mutasi geneB
    jumlah_geneB_mut = round(geneB_mut_prob * len(kromosom_terpilih)) # Menghitung baerapa banyak geneB yang dimutasi
    jumlah_loc_mut = math.ceil(geneB_mut_locus_num * len(kromosom_terpilih)) # Menghitung berapa banyak locus genB yang dimutasi
    
    for i in range(jumlah_geneB_mut):
        r = random.randint(0, len(kromosom_terpilih)-1) # Dipilih genB dalam kromosom r untuk dimutasi

        for j in range(jumlah_loc_mut):
            s = random.randint(0, len(kromosom_terpilih[r][0])-1) # Dipilih locus ke-s dalam geneB kromosom ke-r untuk dimutasi
            kromosom_terpilih[r][0][s] = random.randint(1, len(M))

            while M[kromosom_terpilih[r][0][s]-1] < kumpulan_l[r][s]:
                kromosom_terpilih[r][0][s] = random.randint(1,len(M))

            # Karena geneB termutasi maka geneP termutasi
            kromosom_terpilih[r][1][s] = random.random()


    # Mutasi geneP
    jumlah_geneP_mut = round(geneP_mut_prob * len(kromosom_terpilih)) # Menghitung baerapa banyak geneP yang dimutasi
    jumlah_loc_mut = math.ceil(geneP_mut_locus_num * len(kromosom_terpilih)) # Menghitung berapa banyak locus genP yang dimutasi

    for i in range(jumlah_geneP_mut):
        r = random.randint(0, len(kromosom_terpilih)-1) # Dipilih genP dalam kromosom r untuk dimutasi

        for j in range(jumlah_loc_mut):
            s = random.randint(0, len(kromosom_terpilih[r][1])-1) # Dipilih locus ke-s dalam geneP kromosom ke-r untuk dimutasi
            kromosom_terpilih[r][1][s] = random.random()

    return kromosom_terpilih


def genetic_Algorithm(M:list, l:list, sel_probability, geneB_mut_prob, geneB_locus_num, geneP_mut_prob, geneP_locus_num):
    
    populasi = [] # 1 populasi terdiri dari 6 kromosom
    kromosom = [] # 1 kromosom terdiri dari 2 gen, geneB dan geneP
    kumpulan_l = [l for i in range(6)] # kumpulan l dalam satu populasi
    kumpulan_I = [[] for i in range(6)] # kumpulan I dalam satu populasi
    kumpulan_k = [[] for i in range(6)] # kumpulan k dalam satu populasi

    #Inisialisasi populasi
    for j in range(6):
        kromosom = []
        geneB = []
        geneP = []
        
        for i in range(len(l)):
            geneB.insert(i, random.randint(1,len(M)) )
            while M[geneB[i]-1] < l[i]:
                geneB[i] = random.randint(1,len(M))
        geneP = [round(random.random(),4) for i in range(len(l))]
        kromosom.insert(0,geneB)
        kromosom.insert(1,geneP)
        populasi.insert(j,kromosom)

    y = 0 # yield rate untuk syarat terminate
    z = 0 # generation counter
    while y < 0.9 and z < 1000:

        # Mereset kumpulan_I, kumpulan_k, 
        kumpulan_I = [[] for i in range(6)] # kumpulan I dalam satu populasi
        kumpulan_k = [[] for i in range(6)] # kumpulan k dalam satu populasi
        set_I_tidakDisatuin = [[] for i in range(6)]

        # Kalkulasi Assortment
        ac = []
        
        for i in range(6):
            
            ac.append(assorment_calculation(populasi[i][0], populasi[i][1], kumpulan_l[i], M)) # diperoleh (I, k, geneB, geneP, l) untuk kromosom i
            populasi[i][0] = ac[i][2][:] # geneB pada kromosom i diperbarui
            populasi[i][1] = ac[i][3][:] # geneP pada kromosom i diperbarui
            kumpulan_I[i] = ac[i][0][:] # kumpulan I untuk kromosom i
            kumpulan_k[i] = ac[i][1][:] # kumpulan k untuk kromosom i
            kumpulan_l[i] = ac[i][4][:] # kumpulan l untuk kromosom i
        
        
        # Kalkulasi Nilai Fungsi Fitness
        kumpulan_fitness = []
        for i in range(6):
            kumpulan_fitness.append(fitness(kumpulan_k[i], M, kumpulan_l[i])) # kumpulan nilai fitness suatu kromosom

        # Kalkulasi Snipping Rate dari Mother Material
        kumpulan_snip_p = [] # merupakan kumpulan snip untuk satu populasi, satu kumpulan_snip_p memuat 5 kumpulan_snip
        kumpulan_snip = [] # kumpulan snipping rate dalam satu kromosom
        for i in range(6):
            kumpulan_snip = []
            for j in range(len(M)):
                kumpulan_snip.append(snipping_rate_t(kumpulan_I[i], kumpulan_k[i], M, j))
            kumpulan_snip_p.append(kumpulan_snip) 

        # Revisi geneP
        for i in range(6):
            reviseGeneP(kumpulan_I[i], kumpulan_k[i], M, l, populasi[i][0], populasi[i][1])

        # Selection
        kromosom_terpilih = (selection(populasi, kumpulan_fitness))
        
        # Crossover
        hasil_crossover = crossover(kromosom_terpilih, kumpulan_l, kumpulan_snip_p, populasi, sel_probability)
        kromosom_terpilih.append(hasil_crossover[0])
        kromosom_terpilih.append(hasil_crossover[1])

        # Mutation
        kromosom_terpilih = mutation(kromosom_terpilih, M, kumpulan_l, geneB_mut_prob, geneB_locus_num, geneP_mut_prob, geneP_locus_num)

        populasi = []
        for i in range(len(kromosom_terpilih)):
            populasi.append(kromosom_terpilih[i]) # Diperoleh populasi untuk generasi z+1

######## Uji Hasil
        # Kalkulasi Assortment
        ac = []
            
        for i in range(6):
                
            ac.append(assorment_calculation(populasi[i][0], populasi[i][1], kumpulan_l[i], M)) # diperoleh (I, k, geneB, geneP, l) untuk kromosom i
            populasi[i][0] = ac[i][2][:] # geneB pada kromosom i diperbarui
            populasi[i][1] = ac[i][3][:] # geneP pada kromosom i diperbarui
            kumpulan_I[i] = ac[i][0][:] # kumpulan I untuk kromosom i
            kumpulan_k[i] = ac[i][1][:] # kumpulan k untuk kromosom i
            kumpulan_l[i] = ac[i][4][:] # kumpulan l untuk kromosom i
            set_I_tidakDisatuin[i] = ac[i][5][:]

        # Kalkulasi Nilai Fungsi Fitness

        kumpulan_fitness = []
        for i in range(6):
            kumpulan_fitness.append(fitness(kumpulan_k[i], M, kumpulan_l[i])) # kumpulan nilai fitness suatu kromosom

        # Mencari kromosom dengan nilai fungsi fitness terbesar

        fit = max(kumpulan_fitness)
        kromosom_hasil = populasi[kumpulan_fitness.index(fit)]

        k = kumpulan_k[kumpulan_fitness.index(fit)]
        I = kumpulan_I[kumpulan_fitness.index(fit)]
        I_split = set_I_tidakDisatuin[kumpulan_fitness.index(fit)]

        J = objective(k, M)
        y = yield_rate(l, J)

        z += 1
        



####Memilih solusi akhir####

    # Output
    # print('banyaknya generasi :', z)
    # print('J :', J)
    # print('yield_rate :', yield_rate(l, J))
    # print('M :', M)
    # print('hasil I: ', I)
    # print('hasil k: ', k)
    
    # b = []
    # I_sum = []
    # for i in range(len(M)):
    #     b.append(M[i]*k[i])
    #     I_sum.append(sum(I[i]))

    # print('b : ', b)
    # print('sum I :', I_sum)
    # print('hasil geneB: ', kromosom_hasil[0])
    # print('hasil geneP: ', kromosom_hasil[1])

    return [I, k, y, z, I_split]



######MAIN APP#####

# Diketahui :
# l = [12, 8 ,10, 20, 20, 10, 8] # himpunan panjang produk yang diminta
# M = [20, 10, 12, 8] # himpunan panjang mother material 3.5, 2.7, 2.2, 2.2, 1.9, 1.7, 1.5
# sel_probability = 0.5
# geneB_mut_prob = 0.1
# geneB_mut_locus_num = 0.1
# geneP_mut_prob = 0.1
# geneP_mut_locus_num = 0.1

# M = []
# l = []
#Input
# m = int(input('Input jumlah mother material : ', ))
# jumlah_l = int(input('Input jumlah batang : ',))
# for i in range(m):
#     M.append(int(input(f'Input M[{i}] : ')),)
# for i in range(jumlah_l):
#     l.append(int(input(f'Input l[{i}] : ')),)
# genetic_Algorithm(M, l, sel_probability, geneB_mut_prob, geneB_mut_locus_num, geneP_mut_prob, geneP_mut_locus_num)



#PROGRAM UTAMA

def main_program():
    #inisialisasi
    sel_probability = 0.5
    geneB_mut_prob = 0.1
    geneB_mut_locus_num = 0.1
    geneP_mut_prob = 0.1
    geneP_mut_locus_num = 0.1
    
    #get input dan ubah menjadi list
    mother_len = inputM.get().split(',')
    mother_len = [float(i) for i in mother_len]
    product_len = inputL.get().split(',')
    product_len = [float(i) for i in product_len]

    #gasken
    GA = genetic_Algorithm(mother_len, product_len, sel_probability, geneB_mut_prob,
                      geneB_mut_locus_num, geneP_mut_prob, geneP_mut_locus_num)
    
    #delete previous output
    textI.delete('1.0', 'end')
    textK.delete('1.0', 'end')
    textY.delete('1.0', 'end')
    textZ.delete('1.0', 'end')

    #print value to user
    textI.insert('end', GA[4])
    textK.insert('end', GA[1])
    textY.insert('end', GA[2])
    textZ.insert('end', GA[3])



typeface = 'Segoe UI'
color = {
    'bg' : 'whitesmoke',
    'fg' : 'black',
    'main' : 'mediumseagreen'
}

#GUI
window = tk.Tk()
window.title('Genetic Algorithm for CSP')
window.configure(bg=color['bg'])
window.geometry('650x500+400+50')
window.resizable(False, False)
window.rowconfigure((0), weight = 1)
window.columnconfigure((0,1), weight = 1)
frame1 = tk.Frame(window, bg=color['bg'])
frame1.grid(row=0, column=0, sticky=tk.NS)
frame2 = tk.Frame(window, bg=color['main'])
frame2.grid(row=0, column=1, sticky=tk.NS)

#frame1 content
mainLbl = tk.Label(frame1, text=f'Cutting Stock\nProblem',
                   bg=color['bg'], fg=color['main'],
                   font=(typeface, 28, 'bold')).pack(padx=20, pady=(20,12))
frameInput = tk.Frame(frame1, bg=color['bg'])
frameInput.pack(padx=20, pady=20)
lblM = tk.Label(frameInput, text='m: ',
                   bg=color['bg'], fg=color['fg'],
                   font=(typeface, 12, 'bold')).grid(row=0, column=0, pady=12, sticky=tk.E)
inputM = tk.Entry(frameInput, highlightcolor=color['main'], font=(typeface, 12),highlightthickness=1)
inputM.grid(row=0, column=1, columnspan=3, sticky=tk.EW)
lblM1 = tk.Label(frameInput, text='#Masukkan list\n panjang bahan mentah',
                   bg=color['bg'], fg=color['main'], justify=tk.LEFT,
                   font=(typeface, 8, 'bold')).grid(row=0, column=4, sticky=tk.W)
lblL = tk.Label(frameInput, text='l: ',
                   bg=color['bg'], fg=color['fg'],
                   font=(typeface, 12, 'bold')).grid(row=1, column=0, sticky=tk.E)
inputL = tk.Entry(frameInput, highlightcolor=color['main'], font=(typeface, 12),highlightthickness=1)
inputL.grid(row=1, column=1, columnspan=3, sticky=tk.EW)
lblL1 = tk.Label(frameInput, text='#Masukkan list\n panjang produk',
                   bg=color['bg'], fg=color['main'], justify=tk.LEFT,
                   font=(typeface, 8, 'bold')).grid(row=1, column=4, sticky=tk.W)

buttonConfirm = tk.Button(frame1, text='Konfirmasi', bg=color['main'], fg=color['bg'],
                          relief=tk.FLAT, font=(typeface, 10, 'bold'), command=main_program)
buttonConfirm.pack(padx=20, fill=tk.X)

lblDuide = tk.Label(frame1, text=f'Panduan Input',
                   bg=color['bg'], fg=color['main'],
                   font=(typeface, 18, 'bold')).pack(padx=30, pady=(20,12))
guide1 = tk.Label(frame1, text=f'1. Masukkan input berupa list bilangan yang\n menyatakan panjang, tanpa menuliskan satuan panjang\n2. Gunakan "." (titik) untuk bilangan desimal\n3. Gunakan ","(koma) untuk pemisah antar bilangan',
                   bg=color['bg'], fg=color['fg'], justify=tk.LEFT,
                   font=(typeface, 8)).pack(padx=20)
guide2 = tk.Label(frame1, text=f'Contoh input yang benar:\n   3.5, 4, 10, 0.7, 5.4',
                   bg=color['bg'], fg=color['main'], justify=tk.LEFT,
                   font=(typeface, 8, 'bold')).pack()
#frame2 content
lblResult = tk.Label(frame2, text=f'Hasil',
                   bg=color['main'], fg=color['bg'],
                   font=(typeface, 18, 'bold')).grid(row=0, column=0, columnspan=5, padx=50, pady=(60,12))
lblI = tk.Label(frame2, text='I: ',
                   bg=color['main'], fg=color['bg'],
                   font=(typeface, 12, 'bold')).grid(row=1, column=0, sticky=tk.E)
textI = tk.Text(frame2, relief=tk.FLAT, font=(typeface, 10), width=20, height=3)
textI.grid(row=1, column=1, columnspan=4, padx=(0,12))
lblI1 = tk.Label(frame2, text='#Urutan pemotongan',
                   bg=color['main'], fg=color['bg'],
                   font=(typeface, 8, 'bold')).grid(row=2, column=0, columnspan=5, pady=(0, 8))
lblK = tk.Label(frame2, text='k: ',
                   bg=color['main'], fg=color['bg'],
                   font=(typeface, 12, 'bold')).grid(row=3, column=0, sticky=tk.E)
textK = tk.Text(frame2, relief=tk.FLAT, font=(typeface, 8), width=20, height=2)
textK.grid(row=3, column=1, columnspan=4, padx=(0,12))
lblK1 = tk.Label(frame2, text=f'#Banyaknya bahan mentah\nyang digunakan',
                   bg=color['main'], fg=color['bg'],
                   font=(typeface, 8, 'bold')).grid(row=4, column=0, columnspan=5, pady=(0, 8))
lblY = tk.Label(frame2, text='Y: ',
                   bg=color['main'], fg=color['bg'],
                   font=(typeface, 12, 'bold')).grid(row=5, column=0, sticky=tk.E)
textY = tk.Text(frame2, relief=tk.FLAT, font=(typeface, 8), width=20, height=2)
textY.grid(row=5, column=1, columnspan=2, padx=(0,12))
lblY1 = tk.Label(frame2, text=f'#Yield rate',
                   bg=color['main'], fg=color['bg'],
                   font=(typeface, 8, 'bold')).grid(row=6, column=0, columnspan=5, pady=(0, 8))
lblZ = tk.Label(frame2, text='Z: ',
                   bg=color['main'], fg=color['bg'],
                   font=(typeface, 12, 'bold')).grid(row=7, column=0, sticky=tk.E)
textZ = tk.Text(frame2, relief=tk.FLAT, font=(typeface, 8), width=20, height=2)
textZ.grid(row=7, column=1, columnspan=2, padx=(0,12))
lblZ1 = tk.Label(frame2, text=f'#Generasi',
                   bg=color['main'], fg=color['bg'],
                   font=(typeface, 8, 'bold')).grid(row=8, column=0, columnspan=5, pady=(0, 8))
credit = tk.Label(frame2, text=f'Oleh:\nFachri, Miftah, Reksa',
                   bg=color['main'], fg=color['bg'],
                   font=(typeface, 8, 'bold')).grid(row=8, column=0, columnspan=5, pady=(20, 8))

window.mainloop()