// Placeholder for constraint definitions and their associated graphics
const constraints = {
    none: {
        name: "No Constraint",
        icon: null,
    },
    // Future constraints will be added here
};

export function getConstraint(name) {
    return constraints[name];
}

export function listConstraints() {
    return Object.keys(constraints).map((key) => ({ id: key, ...constraints[key] }));
}
