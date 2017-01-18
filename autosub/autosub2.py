#!/usr/bin/env python
 #coding=utf-8 
from autofundation import *

def within_ranges(time, ranges):
    for r in ranges:
        if time >= r[0] and time <= r[1]:
            return True
    return False

def find_speech_regions(filename, ranges, frame_width=4096):
    print "Ranges:"
    print ranges
    reader = wave.open(filename)
    sample_width = reader.getsampwidth()
    rate = reader.getframerate()
    n_channels = reader.getnchannels()

    total_duration = reader.getnframes() / rate
    chunk_duration = float(frame_width) / rate

    n_chunks = int(total_duration / chunk_duration)
    energies = []

    for i in range(n_chunks):
        chunk = reader.readframes(frame_width)
        energies.append(audioop.rms(chunk, sample_width * n_channels))

    threshold = percentile(energies, 0.6)

    elapsed_time = 0

    regions = []
    region_start = None

    # for energy in energies:
    #     is_silence = energy <= threshold
    #     max_exceeded = region_start and elapsed_time - region_start >= max_region_size
    #     if (max_exceeded or is_silence) and region_start:
    #         if elapsed_time - region_start >= min_region_size:
    #             regions.append((region_start, elapsed_time))
    #         	region_start = None

    #     elif (not region_start) and (not is_silence):
    #         region_start = elapsed_time
    #     elapsed_time += chunk_duration

    # for energy in energies:
    #     is_silence = energy <= threshold
    #     max_exceeded = region_start and elapsed_time - region_start >= max_region_size
    #     if (max_exceeded or is_silence) and region_start:
    #         if elapsed_time - region_start >= min_region_size:
    #             regions.append((region_start, elapsed_time))
    #         	region_start = None

    #     elif (not region_start) and (not is_silence):
    #         region_start = elapsed_time
    #     elapsed_time += chunk_duration

    # Canceled min
    # i=0
    for energy in energies:
        is_silence = energy <= threshold
        # i += 1
        # print i
        # print "elapsed_time: %d"%(elapsed_time)
        # if region_start:
        #     print "start: %d"%(region_start)
        # if is_silence:
        #     print "silence"
        # if within_ranges(elapsed_time,ranges):
        #     print "in ranges"
    
        if is_silence and region_start and within_ranges(region_start,ranges):
            print "here!!!!!!"
            regions.append((region_start, elapsed_time))
            region_start = None

        elif (not region_start) and (not is_silence) and within_ranges(elapsed_time,ranges):
            region_start = elapsed_time
        elapsed_time += chunk_duration
    if region_start and within_ranges(elapsed_time,ranges):
        regions.append((region_start, elapsed_time))
    print regions

    return regions


def autosub2(source_path,  ranges=None, key=None, concurrency=10, output=None, format="json", src_language="en", dst_language="en", api_key=None):

    if format not in FORMATTERS.keys():
        print("Subtitle format not supported. Run with --list-formats to see all supported formats.")
        return 1
    if src_language not in LANGUAGE_CODES.keys():
        print("Source language not supported. Run with --list-languages to see all supported languages.")
        return 1
    if dst_language not in LANGUAGE_CODES.keys():
        print(
            "Destination language not supported. Run with --list-languages to see all supported languages.")
        return 1
    if not source_path: #and not args.video#
        print("Error: You need to specify a source path.")
        return 1

    # if args.video:
    #     print("Transcribe video to audio")
    #     temp = tempfile.NamedTemporaryFile(prefix="audio_", suffix='.flac')
    #     temp_name = temp.name
    #     command = "ffmpeg -i %s -y -ab 160k -ac 1 -ar 44100 -vn %s" %(args.video, temp_name)
    #     subprocess.call(command, shell=True)
    #     source_path = temp_name
    #     output_path = args.video

    source_path = source_path
    output_path = source_path
    audio_filename, audio_rate = extract_audio(source_path)

  
    regions = find_speech_regions(audio_filename,ranges=ranges)
    pool = multiprocessing.Pool(concurrency)
    converter = FLACConverter(source_path=audio_filename)
    recognizer = SpeechRecognizer(language=src_language, rate=audio_rate, api_key=GOOGLE_SPEECH_API_KEY)
    transcripts = []
    if regions:
        try:
            widgets = ["Converting speech regions to FLAC files: ", Percentage(), ' ', Bar(), ' ', ETA()]
            pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()
            extracted_regions = []
            for i, extracted_region in enumerate(pool.imap(converter, regions)):
                extracted_regions.append(extracted_region)
                pbar.update(i)
            pbar.finish()

            widgets = ["Performing speech recognition: ", Percentage(), ' ', Bar(), ' ', ETA()]
            pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()

            for i, transcript in enumerate(pool.imap(recognizer, extracted_regions)):
                transcripts.append(transcript)
                pbar.update(i)
            pbar.finish()

            if not is_same_language(src_language, dst_language):
                if api_key:
                    google_translate_api_key = api_key
                    translator = Translator(dst_language, google_translate_api_key, dst=dst_language,
                                            src=src_language)
                    prompt = "Translating from {0} to {1}: ".format(src_language, dst_language)
                    widgets = [prompt, Percentage(), ' ', Bar(), ' ', ETA()]
                    pbar = ProgressBar(widgets=widgets, maxval=len(regions)).start()
                    translated_transcripts = []
                    for i, transcript in enumerate(pool.imap(translator, transcripts)):
                        translated_transcripts.append(transcript)
                        pbar.update(i)
                    pbar.finish()
                    transcripts = translated_transcripts
                else:
                    print "Error: Subtitle translation requires specified Google Translate API key. \
                    See --help for further information."
                    return 1
        except KeyboardInterrupt:
            pbar.finish()
            pool.terminate()
            pool.join()
            print "Cancelling transcription"
            return 1
    timed_subtitles = [(r, t) for r, t in zip(regions, transcripts) if t]
    formatter = FORMATTERS.get(format)
    formatted_subtitles = formatter(timed_subtitles)
    os.remove(audio_filename)

    return formatted_subtitles

