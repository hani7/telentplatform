"use strict";

document.addEventListener("DOMContentLoaded", function () {
    let resendOTP = document.getElementById("resendOTP");

    if (resendOTP) {
        let optcount = 60;
        let optcounter = setInterval(otptimer, 1000);

        function otptimer() {
            optcount--;

            if (optcount <= 0) {
                clearInterval(optcounter);
                resendOTP.innerHTML = '<a class="resendOTP" href="javascript:void(0)">Resend OTP</a>';
                resendOTP.style.color = "";
            } else {
                resendOTP.innerHTML = 'Wait ' + optcount + ' secs';
                if (optcount <= 10) {
                    resendOTP.style.color = "red";
                } else {
                    resendOTP.style.color = "";
                }
            }
        }
    }
});