# TUGAS BESAR 2 IF3140 Manajemen Basis Data

> Mahasiswa diberikan tugas untuk melakukan eksplorasi dari *Concurrency Control* dan *Recovery*, serta melakukan simulasi terhadap protokol *Concurrency Control*.

<br>

## Eksplorasi *Concurrency Control*
1. Serializability
2. Repeatable Read
3. Read Committed
4. Read Uncommitted

## Simulasi protokol *Concurrency Control*
1. *Simple Locking (exclusive locks only)*
2. *Serial Optimistic Concurrency Control (OCC)*

## Eksplorasi *Recovery*
1. Write-Ahead Log
2. Continuous Archiving
3. Point-in-Time Recovery

<br>
<br>


## Kontributor
<table>
<tr><td colspan = 3 align = "center">K02 G09</td></tr>
<tr><td>No.</td><td>NAMA</td><td>NIM</td></tr>
<tr><td>1.</td><td><a href="https://github.com/roysimbolon"><b>Roy H Simbolon</b></a></td><td>13519068</td></tr>
<tr><td>3.</td><td><a href="https://github.com/danielsalim"><b>Daniel Salim</b></a></td><td>13520008</td></tr>
<tr><td>2.</td><td><a href="https://github.com/VieriMansyl"><b>Vieri Mansyl</b></a></td><td>13520092</td></tr>
<tr><td>4.</td><td><a href="https://github.com/mhilmirinaldi"><b>Mohamad Hilmi Rinaldi</b></a></td><td>13520149</td></tr>
</table>


## Petunjuk penggunaan program

### Program <i>simplelocking.py</i>
1. Masuk ke dalam folder <i>src</i>
```
> cd src
```
2. jalankan program dengan menggunakan <i>command</i> berikut.
```
> py simplelocking.py
```
3. Masukkan <i>schedule</i> yang ingin di-uji coba dengan menggunakan format berikut.
```
FORMAT : [operasi][transaksi]([item data])
contoh : W1(A),C2,R2(D)
```