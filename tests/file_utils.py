import re


class File_utils:

    @staticmethod
    def get_registration_numbers_from_input_file():

        pattern = r'\b[A-Z]{2}\d{2}[A-Z]{3}\b|\b[A-Z]{2}\d{2}\s?[A-Z]{3}\b'
        input_file_path = 'car_input - V6.txt'

        registrations = []
        with open(input_file_path, 'r') as f:
            for line in f:
                registration_numbers = re.findall(pattern, line)
                for reg in registration_numbers:
                    if ' ' in reg:
                        registrations.append(reg)
                    else:
                        formatted_string = re.sub(r'(.{4})', r'\1 ', reg)
                        registrations.append(formatted_string)

        return registrations

    @staticmethod
    def get_details_from_output_file():
        output_dict = {}
        output_file_path = 'car_output - V6.txt'

        with open(output_file_path, 'r') as f:
            next(f)
            for line in f:
                values = line.split(',', maxsplit=1)
                key = values[0]
                val = (values[1].rstrip('\n'))
                output_dict[key] = val

        return output_dict
