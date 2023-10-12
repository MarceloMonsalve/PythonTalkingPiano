# PythonTalkingPiano

This is my talking piano application. It uses the discrete fourier transform to extract the fundamental frequencies of a recording of a human voice. The fft is calcuated every 50 milliseconds and the top 40 frequencies are extracted. Low magnitude frequencies are cut to denoise the signal. Lastly they are converted to MIDI notes. A virtual piano plays the notes back at the appropriate tempo. 
