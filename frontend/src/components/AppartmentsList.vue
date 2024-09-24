<template>
    <v-container>
        <v-row>
            <v-col cols="9">
                <v-card>
                    <v-card-title class="headline"
                        >Liste d'appartements</v-card-title
                    >
                    <v-simple-table class="styled-table">
                        <thead>
                            <tr>
                                <th>Appartement</th>
                                <th>Nombre de pièces</th>
                                <th>Surface (m²)</th>
                                <th>Nombre de fenêtres</th>
                                <th>Prix (€)</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="suite in suites" :key="suite.id">
                                <td>{{ suite.id }}</td>
                                <td>{{ suite.nbRooms }}</td>
                                <td>{{ suite.surface }}</td>
                                <td>{{ suite.nbWindows }}</td>
                                <td>{{ suite.price }}</td>
                                <td>
                                    <v-btn
                                        @click="editSuite(suite)"
                                        color="primary"
                                        class="action-btn"
                                        density="comfortable"
                                        size="small"
                                        icon="mdi-pencil"
                                    >
                                    </v-btn>
                                    <v-btn
                                        @click="deleteSuite(suite.id)"
                                        color="error"
                                        class="action-btn"
                                        density="comfortable"
                                        size="small"
                                        icon="mdi-delete"
                                    >
                                    </v-btn>
                                </td>
                            </tr>
                        </tbody>
                    </v-simple-table>
                </v-card>
            </v-col>
            <v-col cols="3">
                <v-card style="padding: 10px">
                    <v-card-title class="headline">{{
                        editMode
                            ? "Modifier un appartement"
                            : "Ajouter un appartement"
                    }}</v-card-title>
                    <v-form @submit.prevent="submitForm">
                        <v-text-field
                            v-model.number="form.nbRooms"
                            label="Nombre de pièces"
                            type="number"
                            required
                        ></v-text-field>
                        <v-text-field
                            v-model.number="form.surface"
                            label="Surface"
                            type="number"
                            required
                        ></v-text-field>
                        <v-text-field
                            v-model.number="form.nbWindows"
                            label="Nombre de fenêtres"
                            type="number"
                            required
                        ></v-text-field>
                        <v-text-field
                            v-model.number="form.price"
                            label="Prix"
                            type="number"
                            required
                        ></v-text-field>

                        <v-btn type="submit" color="success">
                            {{ editMode ? "Mettre à jour" : "Ajouter" }}
                        </v-btn>
                        <v-btn @click="resetForm" color="error" v-if="editMode">
                            Annuler
                        </v-btn>
                    </v-form>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const suites = ref([]);

onMounted(async () => {
    try {
        const response = await axios.get("http://localhost:3002/suites");
        suites.value = response.data;
        console.log(response.data);
    } catch (error) {
        console.error(error);
    }
});

const form = ref({
    id: null,
    nbRooms: "",
    surface: "",
    nbWindows: "",
    price: "",
});

const editMode = ref(false);

// Ajouter ou mettre à jour un appartement
const submitForm = async () => {
    if (editMode.value) {
        try {
            await axios.patch(`http://localhost:3002/suites/${form.value.id}`, {
                nbRooms: form.value.nbRooms,
                surface: form.value.surface,
                nbWindows: form.value.nbWindows,
                price: form.value.price,
            });
            const index = suites.value.findIndex(
                (suite) => suite.id === form.value.id
            );
            if (index !== -1) {
                suites.value[index] = { ...form.value };
            }
            resetForm();
        } catch (error) {
            console.error(error);
        }
    } else {
        try {
            const response = await axios.post(
                "http://localhost:3002/suites",
                form.value
            );
            form.value.id = response.data.id;
            suites.value.push({ ...form.value });
            resetForm();
        } catch (error) {
            console.error(error);
        }
    }
};

// Remplir le formulaire pour l'édition
const editSuite = (suite) => {
    form.value = { ...suite };
    editMode.value = true;
};

// Supprimer un appartement
const deleteSuite = async (id) => {
    try {
        await axios.delete(`http://localhost:3002/suites/${id}`);
        suites.value = suites.value.filter((suite) => suite.id !== id);
    } catch (error) {
        console.error(error);
    }
};

// Réinitialiser le formulaire après soumission ou annulation
const resetForm = () => {
    form.value = {
        id: null,
        nbRooms: "",
        surface: "",
        nbWindows: "",
        price: "",
    };
    editMode.value = false;
};
</script>

<style scoped>
.styled-table {
    width: 100%;
    border-collapse: collapse;
}

.styled-table th,
.styled-table td {
    border: 1px solid #ddd;
    padding: 8px;
}

.styled-table th {
    background-color: #f2f2f2;
    text-align: left;
}

.styled-table tr:nth-child(even) {
    background-color: #f9f9f9;
}

.styled-table tr:hover {
    background-color: #f1f1f1;
}

.action-btn {
    margin-right: 5px;
    width: 25px;
}
</style>
