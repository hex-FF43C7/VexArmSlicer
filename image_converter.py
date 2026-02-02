import os
try:
    import Pillow
except:
    os.system('python -m pip install Pillow -q')
    import Pillow

try:
    from aspose.svg.imagevectorization import ImageVectorizer, ImageTraceSmoother, BezierPathBuilder
except:
    os.system('python -m pip install aspose -q')
    from aspose.svg.imagevectorization import ImageVectorizer, ImageTraceSmoother, BezierPathBuilder

    
class VectorToPoints:
    pass

class PngToVector:
    def __init__(self, error_threshold=10, max_iterations=20, colors_limit=3, line_width=1.5):
        self._config_path_builder(error_threshold, max_iterations)
        self.path_builder #double check builder

        self._config_vectorizor(colors_limit, line_width)
        self.vectorizer #double check vectorizor
    
    def _config_path_builder(self, error_threshold, max_iterations):
        self.path_builder = BezierPathBuilder()
        self.path_builder.trace_smoother = ImageTraceSmoother(3)
        self.path_builder.error_threshold = error_threshold
        self.path_builder.max_iterations = max_iterations

    
    def _config_vectorizor(self, colors_limit, line_width):
        self.vectorizer = ImageVectorizer()
        self.vectorizer.configuration.path_builder = self.path_builder
        self.vectorizer.configuration.colors_limit = colors_limit
        self.vectorizer.configuration.line_width = line_width

    def convert(self, path_to_input, path_to_output, output_name=None):
        if not os.path.exists(path_to_output):
            os.makedirs(path_to_output)

        if output_name is None:
            output_name = f"{os.path.basename(path_to_input)}-vectorized.svg"

        with vectorizer.vectorize(path_to_input) as document:
            output_file = os.path.join(path_to_output, output_name)
            document.save(output_file)

        return output_file