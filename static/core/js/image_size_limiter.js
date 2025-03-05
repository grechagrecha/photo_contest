const upload_input = $("#upload-input");

upload_input.on("change", () => {
  alert(this.files[0].size);
});
