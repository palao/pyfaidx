import os
import pytest
from pyfaidx import Faidx, Fasta, FetchError

path = os.path.dirname(__file__)
os.chdir(path)

@pytest.fixture
def remove_index():
    yield
    try:
        os.remove('data/genes.fasta.fai')
    except EnvironmentError:
        pass  # some tests may delete this file

def test_buffer_false(remove_index):
    fasta = Fasta('data/genes.fasta', strict_bounds=True)
    expect = 'TTGAAGATTTTGCATGCAGCAGGTGCGCAAGGTGAAATGTTCACTGTTAAA'.lower()
    result = fasta['gi|557361099|gb|KF435150.1|'][100-1:150].seq.lower()
    assert result == expect

def test_buffer_true(remove_index):
    fasta = Fasta('data/genes.fasta', read_ahead=300, strict_bounds=True)
    expect = 'TTGAAGATTTTGCATGCAGCAGGTGCGCAAGGTGAAATGTTCACTGTTAAA'.lower()
    result = fasta['gi|557361099|gb|KF435150.1|'][100-1:150].seq.lower()
    assert result == expect

def test_buffer_exceed(remove_index):
    fasta = Fasta('data/genes.fasta', read_ahead=300, strict_bounds=True)
    expect = 'atgacatcattttccacctctgctcagtgttcaacatctgacagtgcttgcaggatctctcctggacaaatcaatcaggtacgaccaaaactgccgcttttgaagattttgcatgcagcaggtgcgcaaggtgaaatgttcactgttaaagaggtcatgcactatttaggtcagtacataatggtgaagcaactttatgatcagcaggagcagcatatggtatattgtggtggagatcttttgggagaactactgggacgtcagagcttctccgtgaaagacccaagccctctctatgatatgctaagaaagaatcttgtcactttagccactgctactacagcaaagtgcagaggaaagttccacttccagaaaaagaactacagaagacgatatcccc'
    result = fasta['gi|557361099|gb|KF435150.1|'][0:400].seq.lower()
    assert result == expect

@pytest.mark.xfail(raises=FetchError)
def test_bounds_error(remove_index):
    fasta = Fasta('data/genes.fasta', read_ahead=300, strict_bounds=True)
    result = fasta['gi|557361099|gb|KF435150.1|'][100-1:15000].seq.lower()

@pytest.mark.xfail(raises=ValueError)
def test_buffer_value(remove_index):
    Fasta('data/genes.fasta', read_ahead=0.5)