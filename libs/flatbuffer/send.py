import MyNamespace.Person as PersonFB
import flatbuffers

# Create a FlatBuffers builder
builder = flatbuffers.Builder(1024)

# Serialize the named tuple
person = PersonFB.CreatePerson(builder, builder.CreateString("John"), 30)
builder.Finish(person)

# Get the serialized data
serialized_data = builder.Output()

print("DONE")
