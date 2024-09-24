from ..config import logger
from ..builder import CMDJoiner
from ..handlers import BaseFFMPEG
from ..helpers import runner


class AudioProcessing(BaseFFMPEG):

    @runner()
    def add_metadata(self, output_file=None, force_replace=False, **kwargs):
        if not self.metadata['type'] == 'audio':
            logger.error("Method is only allowed for audio files")
            raise ValueError("the method is not callable due to its only support the audio format")

        if output_file is None:
            output_file = f"{self.file_name}_modified{self.file_extension}"
            # log for setting default name for the output

        tags = self.metadata.get('format', {}).get('tags', {})
        _metadata = tag_validator(tags, **kwargs)

        _sequence = CMDJoiner(['ffmpeg'])
        if force_replace:
            _sequence.FORCEFULLY()

        _sequence.INPUT(self.file_path).codec('copy').metadata(**_metadata).OUTPUT_FILE(output_file)
        self.cmd = _sequence.build()


def tag_validator(metadata, **data) -> dict:
    _meta = {}
    for k, v in data.items():
        if metadata[k] == v:
            continue
        _meta[k] = v

    if not _meta:
        logger.warning("Nothing to change")
        raise LookupError("Data is already at the latest version")

    return _meta
