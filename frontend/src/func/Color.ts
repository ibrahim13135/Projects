/**
 * Hash a string to a numeric value.
 * @param str - The input string to be hashed.
 * @returns A numeric hash value.
 */
function hashStringToInt(str: string): number {
let hash = 0;
for (let i = 0; i < str.length; i++) {
hash = str.charCodeAt(i) + ((hash << 5) - hash);
}
return hash;
}

/**
 * Convert a numeric hash to a hexadecimal color code.
 * @param hash - The numeric hash value.
 * @returns A hexadecimal color code.
 */
function intToHexColor(hash: number): string {
// Take the last 6 digits of the hash as a hexadecimal value
const color = ((hash & 0xFFFFFF) >>> 0).toString(16).padStart(6, '0');
return `${color}`;
}

/**
 * Get a unique color from a string.
 * @param str - The input string to generate the color from.
 * @returns A unique hexadecimal color code.
 */
function getColorFromString(str: string): string {
if (!str) return '000000';
const hash = hashStringToInt(str);
return intToHexColor(hash);
}

export default getColorFromString;
