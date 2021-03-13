import collections
from structures import *
from utilities import colored

#verifica se é uma string de DNA
def validateSeq(dna_seq):
    tmpseq = dna_seq.upper()
    for nuc in tmpseq:
        if nuc not in Nucleotides:
            return False
    return tmpseq

#conta a freqência de nuc
def countNucFrequency(seq):
    tmpFreqDict = {"A" : 0,"C" : 0,"G" : 0,"T" : 0}
    for nuc in seq:
        tmpFreqDict[nuc] += 1
    return tmpFreqDict

#otimizando a anterior
def countNucFrequency1(seq):
    return dict(collections.Counter(seq))

#transcrição
def transcription(seq):
    """DNA -> RNA, Transcrição - substitui Timina por Uracilo"""
    return seq.replace("T","U")

#coomplemento inverso
def reverse_complement(seq):
    return ''.join(DNA_ReverseComplement[nuc] for nuc in seq) [::-1]

#reverse complement mais pythonic
def reverse_complement1(seq):
    mapping = str.maketrans('ATCG','TAGC')
    return seq.translate(mapping)[::-1]

#percentua o conteudo GC
def gc_content(seq):
    return round((seq.count('C') + seq.count('G')) / len(seq) * 100)

#semlehante à anterior mas num dado intervalo
def gc_content_subseq(seq, k=20):
    res=[]
    for i in range(0, len(seq) - k + 1, k):
        subseq = seq[i:i + k]
        res.append(gc_content(subseq))
    return res

#traduz DNA em aa
def translate_seq(seq, init_pos=0):
    return [DNA_Codons[seq[pos:pos + 3]] for pos in range(init_pos, len(seq) - 2, 3)]


def codon_usage(seq, aminoacid):
    tmpList = []
    for i in range(0, len(seq) - 2, 3):
        if DNA_Codons[seq[i:i + 3]] == aminoacid:
            tmpList.append(seq[i: i + 3])

    freqDict = dict(collections.Counter(tmpList))
    return freqDict

def gen_reading_frames(seq):
    frames = []
    frames.append(translate_seq(seq, 0))
    frames.append(translate_seq(seq, 1))
    frames.append(translate_seq(seq, 2))
    frames.append(translate_seq(reverse_complement(seq), 0))
    frames.append(translate_seq(reverse_complement(seq), 1))
    frames.append(translate_seq(reverse_complement(seq), 2))

    return frames

def proteins_from_rf(aa_seq):
    current_prot = []
    proteins = []
    for aa in aa_seq:
        if aa == "_":
            if current_prot:
                for p in current_prot:
                    proteins.append(p)
                current_prot = []
        else:
            if aa == "M":
                current_prot.append("")
            for i in range(len(current_prot)):
                current_prot[i] += aa
    return proteins

def all_proteins_from_orfs(seq, startReadPos=0, endReadPos=0, ordered=False):
    if endReadPos > startReadPos:
        rfs = gen_reading_frames(seq[startRead: endRead])
    else: 
        rfs = gen_reading_frames(seq)
        
    res = []
    for rf in rfs:
        prots = proteins_from_rf(rf)
        for p in prots:
            res.append(p)
            
    if ordered:
        return sorted(res, key=len, reverse=True)  
    return res