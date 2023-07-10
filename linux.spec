# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


main_a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[ ('./conf/', './conf/'),
            ('./plugin/', './plugin/'),
            ('./manual/', './manual/'),
            ('./transfer_dog/resource/', './transfer_dog/resource/')],
    hiddenimports=['transfer_worker.utility.logging'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
main_pyz = PYZ(main_a.pure, main_a.zipped_data, cipher=block_cipher)

main_exe = EXE(
    main_pyz,
    main_a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # linux 环境下 icon 配置是无效的
    icon='transfer_dog/resource/app_icon/dog.ico',
)

worker_a = Analysis(
    ['worker.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['transfer_worker.utility.logging'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
worker_pyz = PYZ(worker_a.pure, worker_a.zipped_data, cipher=block_cipher)

worker_exe = EXE(
    worker_pyz,
    worker_a.scripts,
    [],
    exclude_binaries=True,
    name='worker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    main_exe,
    main_a.binaries,
    main_a.zipfiles,
    main_a.datas,

    worker_exe,
    worker_a.binaries,
    worker_a.zipfiles,
    worker_a.datas,
    
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TransferDog',
)