class ScaleValidator:
    def __init__(self):
        # Definición de notas y sus alteraciones
        self.all_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
    def get_scale_notes(self, tonic, scale_type):
        """Genera las notas de la escala basada en la tónica y el tipo"""
        tonic = tonic.upper()
        start_idx = self.all_notes.index(tonic)
        
        # Intervalos para escalas mayores y menores (en semitonos)
        major_intervals = [0, 2, 4, 5, 7, 9, 11]
        minor_intervals = [0, 2, 3, 5, 7, 8, 10]
        
        intervals = major_intervals if scale_type.lower() == 'mayor' else minor_intervals
        scale_notes = []
        
        for interval in intervals:
            note_idx = (start_idx + interval) % 12
            scale_notes.append(self.all_notes[note_idx])
            
        return scale_notes
    
    def get_scale_chords(self, scale_notes, scale_type):
        """Genera los acordes válidos para la escala"""
        valid_chords = set()
        
        # Patrones de acordes según el tipo de escala
        if scale_type.lower() == 'mayor':
            # I, ii, iii, IV, V, vi, vii°
            chord_types = ['', 'm', 'm', '', '', 'm', 'm']
        else:  # menor
            # i, ii°, III, iv, v, VI, VII
            chord_types = ['m', 'm', '', 'm', 'm', '', '']
            
        for i, note in enumerate(scale_notes):
            chord = note + chord_types[i]  # Esto genera el acorde
            valid_chords.add(chord)
            # Agregar séptima si el acorde es menor o mayor
            valid_chords.add(note + chord_types[i] + '7')

            
        return valid_chords
    
    def validate_sequence(self, tonic, scale_type, sequence):
        """Valida una secuencia de notas y acordes"""
        # Obtener notas y acordes válidos
        scale_notes = self.get_scale_notes(tonic, scale_type)
        valid_chords = self.get_scale_chords(scale_notes, scale_type)
        
        # Dividir la secuencia en elementos individuales
        elements = sequence.split()
        
        # Estado inicial del autómata
        current_state = 'q0'
        
        for element in elements:
            # Verificar si el elemento es una nota o acorde
            if len(element) <= 2:  # Es una nota
                if element not in scale_notes:
                    return False, f"Nota inválida: {element}"
            else:  # Es un acorde
                if element not in valid_chords:
                    return False, f"Acorde inválido: {element}"
                    
            # Transición al siguiente estado
            current_state = 'q1'
            
        # Estado final
        return True, "Secuencia válida"

def main():
    validator = ScaleValidator()
    
    # Solicitar entrada del usuario
    tonic = input("Ingrese la tonalidad (ej. C, A, D#): ")
    scale_type = input("Ingrese el tipo de escala (mayor/menor): ")
    sequence = input("Ingrese la secuencia de notas y acordes separados por espacios: ")
    
    # Validar la secuencia
    is_valid, message = validator.validate_sequence(tonic, scale_type, sequence)
    
    # Mostrar resultado
    print(f"\nResultado para {tonic} {scale_type}:")
    print(f"Secuencia: {sequence}")
    print(f"{'Válida' if is_valid else 'Inválida'}: {message}")
    
    # Mostrar información adicional
    scale_notes = validator.get_scale_notes(tonic, scale_type)
    valid_chords = validator.get_scale_chords(scale_notes, scale_type)
    print(f"\nNotas de la escala: {' '.join(scale_notes)}")
    print(f"Acordes válidos: {' '.join(sorted(valid_chords))}")

if __name__ == "__main__":
    main()