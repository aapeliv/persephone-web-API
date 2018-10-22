"""Configration for pytest to run the test suite"""
import pytest

from persephone_api.app import create_app
from persephone_api.extensions import db
from persephone_api.settings import TestConfig, TestConfigCORS

app = create_app(TestConfig)
app_cors = create_app(TestConfigCORS)

# API version prefix
API_VERSION = "v0.1"

# create DB tables
with app.app_context():
    db.create_all()
with app_cors.app_context():
    db.create_all()

# configure upload paths
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #max 64 MB file upload
app_cors.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #max 64 MB file upload

def create_client(tmpdir, app=app):
    """Create a test client to send requests to"""
    uploads_path = tmpdir.mkdir('test_uploads')
    app.config['BASE_UPLOAD_DIRECTORY'] = str(uploads_path)
    corpus_path = tmpdir.mkdir('corpus')
    app.config['CORPUS_PATH'] = str(corpus_path)
    models_path = tmpdir.mkdir('models')
    app.config['MODELS_PATH'] = str(models_path)
    from persephone_api.upload_config import configure_uploads
    configure_uploads(app, base_upload_path=str(uploads_path))
    return app.test_client()

@pytest.fixture
def client(tmpdir):
    with create_client(tmpdir) as c:
        yield c

@pytest.fixture
def client_cors(tmpdir):
    with create_client(tmpdir, app=app_cors) as c:
        yield c

@pytest.fixture
def upload_audio(client):
    """Fixture for convenience in sending requests to the audio endpoint"""
    import wave
    import struct
    import io
    def _make_audio(audio_data, filename: str, framerate: float=44100.00, duration: float=1):
        """Create a file with appropriate WAV magic bytes and encoding

        :audio_data: raw frame data to be placed into the wav file
        :filename: the filename that will be uploaded
        :framerate: hertz
        :duration: seconds this file will go for
        """
        amp = 8000.0 # amplitude
        wav_data = io.BytesIO()
        wav_file = wave.open(wav_data, "wb")
        # wav params
        nchannels = 1
        sampwidth = 2
        framerate = int(framerate)
        nframes = int(framerate*duration)
        comptype = "NONE"
        compname = "not compressed"
        wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        # write the contents
        for s in audio_data:
            wav_file.writeframes(struct.pack('h', int(s*amp/2)))
        wav_file.close()

        # Seek to start of the audio stream data
        wav_data.seek(0)

        data = {'audioFile': (wav_data, filename)}
        return client.post(
            ('/{}/audio'.format(API_VERSION)),
            data=data,
            content_type='multipart/form-data'
        )
        wav_data.close()

    return _make_audio



@pytest.fixture
def upload_transcription(client):
    """Fixture for convenience in sending requests to the transcription endpoint"""
    import io
    def _make_transcription(transcription_data, filename):
        """Create a file with appropriate encoding"""
        data = {'transcriptionFile': (io.BytesIO(transcription_data.encode('utf-8')), filename)}
        return client.post(
            ('/{}/transcription'.format(API_VERSION)),
            data=data,
            content_type='multipart/form-data'
        )

    return _make_transcription


@pytest.fixture
def create_utterance(client):
    """Fixture for convenience in creating an utterance via requests to the utterance specification endpoint"""
    import json
    def _create_utterance(audio_id: int, transcription_id: int):
        """create an utterance from pairs of IDs of resources"""
        data = {
            "audioId": audio_id,
            "transcriptionId": transcription_id
        }

        return client.post(
            '/{}/utterance'.format(API_VERSION),
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
    return _create_utterance


@pytest.fixture
def create_sine():
    def _create_sine(note: str="A", seconds: float=1, framerate: float=44100.00) -> list:
        """Create a sine wave representing the frequency of a piano note
        in octave 4 using the A440 tuning"""
        import math

        note_to_freq = {
            "C": 261.63,
            "C♯": 277.18, "D♭": 277.18,
            "D": 293.66,
            "E♭": 311.13, "D♯": 311.13,
            "E": 329.63,
            "F": 349.23,
            "F♯": 369.99, "G♭": 369.99,
            "G": 392.00,
            "A♭": 415.30, "G♯": 415.30,
            "A": 440.00,
            "B♭": 466.16, "A♯": 466.16,
            "B": 493.88,
        }
        datasize = int(seconds * framerate)
        freq = note_to_freq[note]
        sine_list=[]
        for x in range(datasize):
            sine_list.append(math.sin(2*math.pi * freq * ( x/framerate)))
        return sine_list
    return _create_sine