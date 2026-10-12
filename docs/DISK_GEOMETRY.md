# Disk Geometry

Target 1.44 MB 3.5-inch floppy image:
- 80 cylinders
- 2 heads
- 18 sectors per track
- 512 bytes per sector
- 2,880 sectors
- 1,474,560 bytes

`total_sectors = cylinders * heads * sectors_per_track`
`image_bytes = total_sectors * bytes_per_sector`

CHS sector indices start at 1. CHS (0,0,2) maps to LBA 1.
