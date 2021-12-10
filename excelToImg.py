import excel2img
dir(excel2img)

# Save as PNG the range of used cells in test.xlsx on page named "Sheet1"
excel2img.export_img("result/table_1.xlsx", "result/table_1.png", "Sheet1", None)
