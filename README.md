# azure-image-scanning

Exploring scanning image files for viruses, text, etc.

This processing can be done on Linux VMS, in AKV, with containerized Python code.

## Virus Scanning Test

This test scans several representative images for viruses with the open-source ClamAV library.
Processing time on a desktop computer takes 1-2 milliseconds per image.

```
$ python main.py virus_scan img

virus_scan, directory:  img
connecting to clamd at: /tmp/clamd.socket
clamd version: ClamAV 0.105.1/26625/Fri Aug 12 03:52:45 2022
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/IMG_7152b.jpeg': ('OK', None)}, milliseconds: 1
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/IMG_7154.jpeg': ('OK', None)}, milliseconds: 1
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/IMG_7152.jpeg': ('OK', None)}, milliseconds: 1
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/IMG_7153.jpeg': ('OK', None)}, milliseconds: 1
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/home3.png': ('OK', None)}, milliseconds: 2
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/home2.png': ('OK', None)}, milliseconds: 1
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/sampletext1-ocr-539x450.png': ('OK', None)}, milliseconds: 1
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/home1.png': ('OK', None)}, milliseconds: 1
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/home5.png': ('OK', None)}, milliseconds: 2
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/home4.png': ('OK', None)}, milliseconds: 1
virus scan result: {'/Users/cjoakim/github/azure-image-scanning/img/home6.png': ('OK', None)}, milliseconds: 2
```

See the ClamAV section below for details about this library, installing it, using it.

## Text Extraction Test



### Tesseract

- https://pypi.org/project/pytesseract/

### Installing tesseract on macOS

Installation tests are similar on Linux for AKV.

```
$ brew install tesseract
- or -
$ brew install tesseract --all-languages

$ which tesseract
/usr/local/bin/tesseract

$ tesseract --list-langs
List of available languages in "/usr/local/share/tessdata/" (3):
eng
osd
snum
```

---

###

- https://python-bloggers.com/2022/05/extract-text-from-image-using-python/

### ClamAV

ClamAV® is an open-source antivirus engine for detecting trojans, viruses, malware & other malicious threats.

- https://www.clamav.net
- https://pypi.org/project/clamd/
- https://hub.docker.com/r/clamav/clamav
- https://gist.github.com/mendozao/3ea393b91f23a813650baab9964425b9


### Installing ClamAV and freshclam on macOS

Installation tests are similar on Linux for AKV.

```
$ brew install clamav
    ...
    To finish installation & run clamav you will need to edit
    the example conf files at /usr/local/etc/clamav/

$ cd /usr/local/etc/clamav/
    [/usr/local/etc/clamav]$ ls -al
    -rw-r--r--   1 cjoakim  admin  27171 Aug 12 14:19 clamd.conf.sample
    -rw-r--r--   1 cjoakim  admin   7205 Aug 12 14:19 freshclam.conf.sample

$ cp freshclam.conf.sample freshclam.conf && cp clamd.conf.sample clamd.conf

$ ls -al
    -rw-r--r--   1 cjoakim  admin  27171 Aug 12 14:21 clamd.conf
    -rw-r--r--   1 cjoakim  admin  27171 Aug 12 14:19 clamd.conf.sample
    -rw-r--r--   1 cjoakim  admin   7205 Aug 12 14:21 freshclam.conf
    -rw-r--r--   1 cjoakim  admin   7205 Aug 12 14:19 freshclam.conf.sample

$ freshclam
Creating missing database directory: /usr/local/Cellar/clamav/0.105.1/share/clamav
ClamAV update process started at Fri Aug 12 14:24:05 2022
daily database available for download (remote version: 26625)
Time:   16.4s, ETA:    0.0s [========================>]   56.70MiB/56.70MiB
Testing database: '/usr/local/Cellar/clamav/0.105.1/share/clamav/tmp.71c248f4d0/clamav-6aebc9f04feb7f8e647e30dd19273a15.tmp-daily.cvd' ...
Database test passed.
daily.cvd updated (version: 26625, sigs: 1996254, f-level: 90, builder: raynman)
main database available for download (remote version: 62)
Time:   47.2s, ETA:    0.0s [========================>]  162.58MiB/162.58MiB
Testing database: '/usr/local/Cellar/clamav/0.105.1/share/clamav/tmp.71c248f4d0/clamav-bc122c6a35e3562c10cf8725b8925d15.tmp-main.cvd' ...
Database test passed.
main.cvd updated (version: 62, sigs: 6647427, f-level: 90, builder: sigmgr)
bytecode database available for download (remote version: 333)
Time:    0.3s, ETA:    0.0s [========================>]  286.79KiB/286.79KiB
Testing database: '/usr/local/Cellar/clamav/0.105.1/share/clamav/tmp.71c248f4d0/clamav-dd64a31cbf63f64474f5c3a3a410855a.tmp-bytecode.cvd' ...
Database test passed.
bytecode.cvd updated (version: 333, sigs: 92, f-level: 63, builder: awillia2)

$ brew ls clamav
/usr/local/Cellar/clamav/0.105.1/.bottle/etc/ (2 files)
/usr/local/Cellar/clamav/0.105.1/bin/clamav-config
/usr/local/Cellar/clamav/0.105.1/bin/clambc
/usr/local/Cellar/clamav/0.105.1/bin/clamconf
/usr/local/Cellar/clamav/0.105.1/bin/clamdscan
/usr/local/Cellar/clamav/0.105.1/bin/clamdtop
/usr/local/Cellar/clamav/0.105.1/bin/clamscan
/usr/local/Cellar/clamav/0.105.1/bin/clamsubmit
/usr/local/Cellar/clamav/0.105.1/bin/freshclam
/usr/local/Cellar/clamav/0.105.1/bin/sigtool
/usr/local/Cellar/clamav/0.105.1/include/ (4 files)
/usr/local/Cellar/clamav/0.105.1/lib/libclamav.9.1.0.dylib
/usr/local/Cellar/clamav/0.105.1/lib/libclammspack.0.8.0.dylib
/usr/local/Cellar/clamav/0.105.1/lib/libclamunrar.9.1.0.dylib
/usr/local/Cellar/clamav/0.105.1/lib/libclamunrar_iface.9.1.0.dylib
/usr/local/Cellar/clamav/0.105.1/lib/libfreshclam.2.0.2.dylib
/usr/local/Cellar/clamav/0.105.1/lib/pkgconfig/libclamav.pc
/usr/local/Cellar/clamav/0.105.1/lib/ (12 other files)
/usr/local/Cellar/clamav/0.105.1/sbin/clamd
/usr/local/Cellar/clamav/0.105.1/share/clamav/ (4 files)
/usr/local/Cellar/clamav/0.105.1/share/doc/ (124 files)
/usr/local/Cellar/clamav/0.105.1/share/man/ (13 files)

To start the clamd daemon, run the following:
$ /usr/local/Cellar/clamav/0.105.1/sbin/clamd

$ /usr/local/Cellar/clamav/0.105.1/sbin/clamd &
[1] 41984

$ ps aux | grep clamd
cjoakim          41985 100.0  3.6  6104784 1217248   ??  Rs    2:37PM   0:13.50 /usr/local/Cellar/clamav/0.105.1/sbin/clamd
cjoakim          41987   0.0  0.0  4399300    748 s000  S+    2:37PM   0:00.00 grep clamd
cjoakim          41984   0.0  0.0  4424104   2680 s000  S     2:37PM   0:00.01 /usr/local/Cellar/clamav/0.105.1/sbin/clamd

You should now be able to scan a file by doing:
$ clamdscan /some/location/myfile.txt

$ clamdscan home5.png
/Users/cjoakim/github/cj-ms/gbb/customers/conduent/pyplay/img/home5.png: OK

----------- SCAN SUMMARY -----------
Infected files: 0
Time: 0.039 sec (0 m 0 s)
Start Date: 2022:08:12 14:39:01
End Date:   2022:08:12 14:39:01
```