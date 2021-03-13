from DNAToolKit import *
import random 
from utilities import colored
#cria DNA aleatório para teste com 20 carateres
randDNAStr = ''.join([random.choice(Nucleotides) 
                    for nuc in range(50)])

DNAStr = validateSeq(randDNAStr)

print(f'\nSequence: {DNAStr}\n')
print(f'[1] + Sequence Length: {len(DNAStr)}\n')
print(f'[2] + Nucleotide Frequency: {countNucFrequency(DNAStr)}\n')

print(f'[3] + Transcription: {transcription(DNAStr)}\n')

print(f"[4] + DNA String + Reverse Complement:\n5' {DNAStr} 3'")
print(f"   {''.join(['|' for c in range (len(DNAStr))])}")
print(f"3' {reverse_complement(DNAStr)[::-1]} 5' [Complement]")
print(f"5' {reverse_complement(DNAStr)} 5' [Reverse Complement]\n")

print(f'[5] + GC Content: {gc_content(DNAStr)}%\n')
print(f'[6] + GC Content in Subsection k=5: {gc_content_subseq(DNAStr, k=5)}\n')

print(f'[7] + Aminoacids Sequence from DNA: {translate_seq(DNAStr, 0)}\n')
print(f'[8] + Codon Count (L): {codon_usage(DNAStr, "L")}\n')

print(f'[9] + Reading Frames:')
for frame in gen_reading_frames(DNAStr):
    print(frame)
    
print('\n[10] + All prots in 6 open reading frames:')
for prot in all_proteins_from_orfs(DNAStr, 0, 0, True):
    print(f'{prot}')