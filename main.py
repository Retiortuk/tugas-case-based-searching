import random
import math

# 1. PARAMETER GA & KRITERIA PENGHENTIAN
POP_SIZE = 50       # Ukuran populasi
GEN_MAX = 100       # Kriteria penghentian (maksimal generasi)
PC = 0.8            # Probabilitas Crossover (Pc)
PM = 0.05           # Probabilitas Mutasi (Pm)
BIT_LEN = 10        # Panjang bit per variabel (Total 20 bit per kromosom)
X_MIN = -10.0       # Batas bawah domain
X_MAX = 10.0        # Batas atas domain

# Fungsi Objektif Mencari Minimum
def objective_function(x1, x2):
    try:
        # Interpretasi \sqrt{x_2}^2 adalah nilai mutlak x2 (akar dari kuadrat) untuk menghindari error domain pada x2 negatif
        term1 = math.sin(x1) * math.cos(x2) * math.tan(x1 + x2)
        term2 = 0.5 * math.exp(1 - math.sqrt(x2**2))
        return -(term1 + term2)
    except:
        return float('inf') # Proteksi jika tan(x1+x2) infinity

# 2. INISIALISASI POPULASI
def init_population(pop_size, bit_len):
    population = []
    for _ in range(pop_size):
        # Kromosom biner: 10 bit x1 + 10 bit x2
        chromosome = [random.randint(0, 1) for _ in range(bit_len * 2)]
        population.append(chromosome)
    return population

# 3. DEKODE KROMOSOM
def decode(chromosome, bit_len, x_min, x_max):
    # Pisahkan gen x1 dan x2
    bin_x1 = chromosome[:bit_len]
    bin_x2 = chromosome[bit_len:]
    
    # Hitung nilai desimal
    dec_x1 = sum([val * (2**i) for i, val in enumerate(reversed(bin_x1))])
    dec_x2 = sum([val * (2**i) for i, val in enumerate(reversed(bin_x2))])
    
    # Rumus dekode ke rentang [x_min, x_max]
    max_dec = (2**bit_len) - 1
    x1 = x_min + ((x_max - x_min) * dec_x1 / max_dec)
    x2 = x_min + ((x_max - x_min) * dec_x2 / max_dec)
    
    return x1, x2

# 4. PERHITUNGAN FITNESS (Evaluasi)
def evaluate_population(population):
    fitness_list = []
    for chrom in population:
        x1, x2 = decode(chrom, BIT_LEN, X_MIN, X_MAX)
        obj_val = objective_function(x1, x2)
        # Karena mencari minimum, nilai fungsi objektif langsung kita pakai. 
        # (Lebih kecil = lebih baik)
        fitness_list.append(obj_val) 
    return fitness_list

# 5. PEMILIHAN ORANGTUA (Tournament Selection)
def tournament_selection(population, fitness_list, k=3):
    selected = random.sample(range(len(population)), k)
    best_idx = selected[0]
    for idx in selected[1:]:
        # Memilih nilai yang paling KECIL (minimum)
        if fitness_list[idx] < fitness_list[best_idx]:
            best_idx = idx
    return population[best_idx]

# 6. CROSSOVER (Pindah Silang)
def crossover(parent1, parent2, pc):
    if random.random() < pc:
        # Single-point crossover
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1[:], parent2[:]

# 7. MUTASI
def mutate(chromosome, pm):
    for i in range(len(chromosome)):
        if random.random() < pm:
            chromosome[i] = 1 if chromosome[i] == 0 else 0
    return chromosome

# 8. PERGANTIAN GENERASI (Main GA Loop dengan Elitism)
def run_ga():
    pop = init_population(POP_SIZE, BIT_LEN)
    
    best_overall_chrom = None
    best_overall_val = float('inf')
    
    for generation in range(GEN_MAX):
        fitness_list = evaluate_population(pop)
        
        # Cari individu terbaik di generasi ini (Elitism)
        min_fit_idx = fitness_list.index(min(fitness_list))
        best_gen_chrom = pop[min_fit_idx]
        best_gen_val = fitness_list[min_fit_idx]
        
        if best_gen_val < best_overall_val:
            best_overall_val = best_gen_val
            best_overall_chrom = best_gen_chrom[:]
            
        new_pop = []
        # Elitism: Masukkan 2 kromosom terbaik dari generasi sekarang ke generasi baru
        new_pop.append(best_gen_chrom[:])
        new_pop.append(best_gen_chrom[:])
        
        # Buat sisa populasi
        while len(new_pop) < POP_SIZE:
            p1 = tournament_selection(pop, fitness_list)
            p2 = tournament_selection(pop, fitness_list)
            
            c1, c2 = crossover(p1, p2, PC)
            
            c1 = mutate(c1, PM)
            c2 = mutate(c2, PM)
            
            new_pop.append(c1)
            if len(new_pop) < POP_SIZE:
                new_pop.append(c2)
                
        pop = new_pop
        
    return best_overall_chrom, best_overall_val

# Eksekusi Program
best_chrom, best_val = run_ga()
best_x1, best_x2 = decode(best_chrom, BIT_LEN, X_MIN, X_MAX)

# Output Program
print("===== HASIL OPTIMASI ALGORITMA GENETIKA =====")
print(f"Kromosom Terbaik: {best_chrom}")
print(f"Nilai x1       : {best_x1:.6f}")
print(f"Nilai x2       : {best_x2:.6f}")
print(f"Nilai Minimum  : {best_val:.6f}")