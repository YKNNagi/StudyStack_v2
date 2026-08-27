const tagSelect = document.getElementById("id_tags");
const selectedTags = document.getElementById("selected-tags");

let previousSelectedOptions = Array.from(tagSelect.selectedOptions);

tagSelect.addEventListener("change", function() {

    console.log(tagSelect.selectedOptions.length);
    if (tagSelect.selectedOptions.length > 2) {

    for (const option of tagSelect.options) {
        option.selected = previousSelectedOptions.includes(option);
    }

    } else {

        previousSelectedOptions = Array.from(tagSelect.selectedOptions);

    }

    selectedTags.innerHTML = "";

    for (const option of tagSelect.selectedOptions) {

        const chip = document.createElement("span");

        chip.classList.add("tag-chip");
        chip.textContent = option.text;

        selectedTags.appendChild(chip);
    }

});