"use strict";

document.addEventListener("DOMContentLoaded", function () {
    let otpInputGroup = document.querySelector(".otp-input-group");

    if (!otpInputGroup) return;

    otpInputGroup.addEventListener("keyup", function (e) {
        let t = e.target,
            maxLength = parseInt(t.getAttribute("maxlength"), 10),
            valueLength = t.value.length;

        if (valueLength >= maxLength) {
            let next = t.nextElementSibling;
            while (next) {
                if (next.tagName.toLowerCase() === "input") {
                    next.focus();
                    break;
                }
                next = next.nextElementSibling;
            }
        } else if (valueLength === 0) {
            let prev = t.previousElementSibling;
            while (prev) {
                if (prev.tagName.toLowerCase() === "input") {
                    prev.focus();
                    break;
                }
                prev = prev.previousElementSibling;
            }
        }
    });
});